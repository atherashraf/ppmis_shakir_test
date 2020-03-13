import datetime
import json
import logging
import os
import sys
import time
import traceback
import json
from importlib import import_module
from re import finditer

from django.apps import apps
from django.conf.global_settings import SESSION_ENGINE
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sites import requests
from django.db import connections
from django.urls import reverse
from django.utils.safestring import mark_safe

from digitalarz.local_settings import CONNECTION_KEY_TESTS, MODEL_FIELD_TYPES
from digitalarz.settings import EMAIL_HOST_USER, INSTALLED_APPS, MEDIA_ROOT


class Session_Utils():
    @classmethod
    def get_session(cls, session_key):
        engine = import_module(SESSION_ENGINE)
        return engine.SessionStore(session_key)

    @classmethod
    def delete_session_cache(cls, session_key):
        engine = import_module(SESSION_ENGINE)
        engine.SessionStore(session_key).delete()

    @classmethod
    def get_session_user(cls, session_key):
        session = Session.objects.get(session_key=session_key)
        uid = session.get_decoded().get('_auth_user_id')
        return User.objects.get(pk=uid)


class Common_Utils():
    @classmethod
    def handle_uploaded_file(cls, f):
        file_name = os.path.join(MEDIA_ROOT, "wmp", str(f))
        print(file_name)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        with open(file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_name

    @classmethod
    def json_converter(cls, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()
        else:
            return o

    @classmethod
    def get_project_app(cls):
        proj_app = []
        # for app in INSTALLED_APPS:
        for app in apps.get_app_configs():
            proj_app.append(app.label)

        return proj_app

    @classmethod
    def camel_case_split(cls, identifier):
        matches = finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
        return [m.group(0) for m in matches]

    @classmethod
    def create_name_from_string(cls, text):
        deliminators = ['_', '-', '__']
        for deliminator in deliminators:
            text = text.replace(deliminator, " ")
        words = cls.camel_case_split(text)
        res_string = text if len(words) == 0 else ""
        for word in words:
            res_string = res_string + word
        return res_string

    @classmethod
    def shorten_url(url):
        post_url = 'https://www.googleapis.com/urlshortener/v1/url?key={}'.format(
            'AIzaSyDBKox6Urc8SUwws9mXT9zJFaDbQlN0FL8')
        payload = {'longUrl': url}
        headers = {'content-type': 'application/json'}
        r = requests.post(post_url, data=json.dumps(payload), headers=headers)
        url_dict = r.json()
        return url_dict['id']

    @classmethod
    def get_time_in_miliseconds(cls):
        millis = int(round(time.time() * 1000))
        return millis

    @classmethod
    def createAuthUser(cls, request, username, email, is_staff=False):
        try:
            rand_pass = "testpucit"  # get_random_string()
            auth_user_obj = User.objects.filter(username=username, email=email).first()
            if auth_user_obj is None:
                auth_user_obj = User.objects.create_user(username=username, email=email, password=rand_pass,
                                                         is_staff=is_staff)
            else:
                messages.add_message(request, messages.INFO, mark_safe("%s  auth user already exist " % username))
            # auth_user_obj.set_password(rand_pass)
            reset_password = True
            reset_form = PasswordResetForm({'email': email})
            assert reset_form.is_valid()
            if request:
                reset_form.save(
                    request=request,
                    use_https=request.is_secure(),
                    subject_template_name='registration/password_reset_subject.txt',
                    email_template_name='registration/password_reset_email.html',
                )
            else:
                reset_form.save(from_email=EMAIL_HOST_USER)
        except Exception as e:
            Log_Error.log_view_error_message(request, e)
        return auth_user_obj

    @classmethod
    def get_memory_size(cls, obj, seen=None):
        """Recursively finds size of objects"""
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        # Important mark as seen *before* entering recursion to gracefully handle
        # self-referential objects
        seen.add(obj_id)
        if isinstance(obj, dict):
            size += sum([cls.get_memory_size(v, seen) for v in obj.values()])
            size += sum([cls.get_memory_size(k, seen) for k in obj.keys()])
        elif hasattr(obj, '__dict__'):
            size += cls.get_memory_size(obj.__dict__, seen)
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            size += sum([cls.get_memory_size(i, seen) for i in obj])
        return size


class Log_Error():
    @classmethod
    def log_view_error_message(cls, request, e, act_log=None, redirect_path=None):

        error_message = str(e)
        cls.log_error_message(e, act_log)
        if request:
            messages.add_message(request, messages.ERROR, error_message)
            if redirect_path is None:
                redirect_path = request.META.get('HTTP_REFERER', '')
                if redirect_path == '':
                    redirect_path = "/"
            return redirect_path

        # response.write(error_message)

    @classmethod
    def log_error_message(cls, e, act_log=None):
        error_message = str(e)
        logger = logging.getLogger()
        if act_log is not None: act_log.update_error_desc(error_message)
        logger.error(traceback.format_exc())
        return error_message

    @classmethod
    def log_message(cls, msg):
        logger = logging.getLogger()
        logger.error(msg)


class DB_Query(object):
    @classmethod
    def get_connection_key(cls, app_label, model_name=None, table_name=None):
        for key in CONNECTION_KEY_TESTS:
            if app_label in CONNECTION_KEY_TESTS[key]['APPS']:
                return CONNECTION_KEY_TESTS[key]['DB_KEY']
        return 'default'

    @classmethod
    def execute_query_as_list(self, query, app_label='default'):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            result_list = list(cursor.fetchall())
            cursor.close()
        return result_list

    @classmethod
    def execute_query_as_dict(self, query, is_geom_include=True, app_label='default', model_name=None):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            if is_geom_include:
                result_dict = DB_Query.dictfetchall(cursor)
            else:
                result_dict = DB_Query.dictfetchallXGeom(cursor)
            cursor.close()
        return result_dict

    @classmethod
    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def dictfetchallXGeom(self, cursor):
        columns = []
        for col in cursor.description:
            if col[0] != "geom":
                columns.append(col[0])
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def execute_query_as_one(self, query, is_one=True, app_label='default', model_name=None):
        connection_name = DB_Query.get_connection_key(app_label, model_name)
        connection = connections[connection_name]
        result = None
        with connection.cursor() as cursor:
            cursor.execute(query)
            cur_res = cursor.fetchone()
            if cur_res is not None:
                result = cur_res[0]
            cursor.close()
        return result

    @classmethod
    def execute_dml(self, query, app_label='default'):
        connection_name = DB_Query.get_connection_key(app_label)
        connection = connections[connection_name]
        cursor = connection.cursor()
        res = cursor.execute(query)
        return res

    @classmethod
    def execute_query_as_geojson(cls, query, app_label='gis', geom_col='geom'):
        geo_json_query = "SELECT jsonb_build_object(" \
                         "'type',     'FeatureCollection'," \
                         "'features', jsonb_agg(feature)) " \
                         "FROM ( " \
                         "SELECT jsonb_build_object( " \
                         "'type', 'Feature', " \
                         "'geometry',   ST_AsGeoJSON(%s)::jsonb," \
                         "'properties', to_jsonb(row) - 'geom' -'geometry'" \
                         ") AS feature " \
                         "FROM (%s) row) features;" % (geom_col, query)
        result = DB_Query.execute_query_as_one(geo_json_query, app_label=app_label)
        return result

    @classmethod
    def get_jqx_fields_and_cols_info(cls, table_name, app_label='default'):
        try:
            connection_name = DB_Query.get_connection_key(app_label)
            connection = connections[connection_name]
            cursor = connection.cursor()
            table_description = connection.introspection.get_table_description(cursor, table_name)
            pk_col = connection.introspection.get_primary_key_column(cursor, table_name)
            fields = []
            columns = []
            for row in table_description:
                field_type = connection.introspection.get_field_type(row.type_code, row)
                col_type = "string"
                for key in MODEL_FIELD_TYPES:
                    if field_type in MODEL_FIELD_TYPES[key]:
                        col_type = key
                        break;
                if col_type != "spatial":
                    col_name = row.name  # if row.name != pk_col else "pk"
                    col_size = 60 if col_type == "number" else 150  # row.internal_size * 2 if col_size and col_size >= 50 else col_size = 50
                    fields.append({"name": col_name, "type": col_type})
                    columns.append({"text": col_name, "datafield": col_name, "width": col_size})
            return {"pk_col": pk_col, "fields": fields, "columns": columns}
        except Exception as e:
            Log_Error.log_error_message(e)
            return None


class Model_Utils():
    @classmethod
    def get_model_filter_result_dict(cls, app_label, model_name, field_value, field_name='id'):
        model = apps.get_model(app_label=app_label, model_name=model_name)
        res = list(model.objects.filter(**{field_name: field_value}).values())
        return res


class Context_Utils():
    @classmethod
    def get_user_items(cls, user):
        user_items = [];
        options = {
            "manage": {"name": "Manage", "href": "/admin/", "icon": "fa fa-database"},
            # "manage_spatial": {"name": "Manage Spatial Data", "href": "/spatial_data_admin/",
            #                    "icon": "fa fa-database"},
            "signout": {'name': 'Sign out', 'href': '/accounts/logout/', 'icon': 'fa fa-sign-out'}
        }
        if user.is_superuser:
            for key in options:
                user_items.append(options[key])
        return user_items

    @classmethod
    def get_navbar_items(cls, user):
        navbaritems = []
        options = {
            "home": {'name': 'Home', 'href': '/', 'icon': "fa fa-home"},
            # "wmp": {'name': 'WMP', 'href': reverse('weather_view'), 'icon': 'fa fa-sun-o', 'color': "#f3f71196"}
        };
        if user.is_superuser:
            for key in options:
                navbaritems.append(options[key])
        return navbaritems
