
const statusbarHeight = 25;
const toolbarHeight = 65;
const drawerWidth = 240;



const appBar = (theme) => ({
    // background: 'linear-gradient(90deg, ' + appbarColor1 + ' 40%, ' + appbarColor2 + ' 80%, ' + appbarColor3 + ')',
    border: 0,
    borderRadius: 3,
    boxShadow: '0 3px 5px 2px rgba(0, 0, 0, .3)',
    color: 'white',
    padding: '0 30px',
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
});
export const styles = (theme) => {
    // alert(theme.spacing(1));
    return ({
        root: {
            display: 'flex',
            flexGrow: 1,
            padding: '0px !important',
            margin: '0px !important',
            minHeight: `calc(100vh - ${toolbarHeight}px - ${statusbarHeight}px  )`,
        },
        hide: {
            display: 'none',
        },
        // title: {
        //     flexGrow: 1,
        // },
        bottomTitle: {
            flexGrow: 1,
            textAlign: 'center',
            fontSize: '0.7rem',
        },
        menuButton: {
            marginRight: 36,
        },
        appBarTop: {
            ...appBar(theme),
            height: toolbarHeight + '!important',
            position: 'fixed',
            top: '0px',

        },
        appBarBottom: {
            ...appBar(theme),
            top: 'auto',
            bottom: '0px',
            height: statusbarHeight,
            flexGrow: 1,
        },
        appBarShift: {
            marginLeft: drawerWidth,
            width: `calc(100% - ${drawerWidth}px)`,
            transition: theme.transitions.create(['width', 'margin'], {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.enteringScreen,
            }),
        },


        drawer: {
            // width: '20px !important',
            flexShrink: 0,
            whiteSpace: 'nowrap',
        },
        drawerOpen: {
            width: drawerWidth,
            transition: theme.transitions.create('width', {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.enteringScreen,
            }),
        },
        drawerClose: {
            transition: theme.transitions.create('width', {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.leavingScreen,
            }),
            overflowX: 'hidden',
            width: theme.spacing(7) + 1,
            [theme.breakpoints.up('sm')]: {
                width: theme.spacing(9) + 1,
            },
        },
        // drawerHeader: {
        //     display: 'flex',
        //     alignItems: 'center',
        //     // color: color,
        //     padding: theme.spacing(0, 1),
        //     // ...theme.mixins.toolbar,
        //     // backgroundColor: appbarColor1,
        //     minHeight: toolbarHeight + "px !important"
        // },
        // drawerFooter: {
        //     // position:'absolute',
        //     height: statusbarHeight,
        //     // color: color,
        //     // backgroundColor: appbarColor1,
        //     bottom: 0,
        //     // top:'auto',
        // },
        // drawerSideNavbar: {
        //     width: drawerWidth - 1,
        //     height: '100vh',
        //     overflowY: 'auto',
        //     margin: '0px',
        //     padding: '0px',
        //     // backgroundColor: appDefaultColor
        // },

    });
}

