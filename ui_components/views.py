from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from digitalarz.utils import DB_Query, Log_Error



def get_jqx_grid_table_data(request, table_name):

    res = DB_Query.get_jqx_fields_and_cols_info(table_name)
    if res is not None:
        sel_list = ""
        for field in res["fields"]:
            sel_list = sel_list + ' "' + field["name"] + '",'
        data = []
        if len(sel_list) > 0:
            sel_list = sel_list[:len(sel_list) - 1]
            query = "Select %s from %s" % (sel_list, table_name)
            res["data"] = DB_Query.execute_query_as_dict(query, False)
        res = {"status": 200, "payload": res}
        return JsonResponse(res)


