import * as React from "react";

import TextField from "@material-ui/core/TextField";
import Container from "@material-ui/core/Container";

import {styles} from "../../molecules/static/styles/materialui-styles"

import {withStyles} from '@material-ui/core/styles';

// let appStore = new AppStore()
//
// baseTemplate(config, appStore)

class SignInFormPage extends React.PureComponent {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <Container maxWidth="sm" style={{"textAlign": "center", "paddingTop": "100px"}}>
                <TextField fullWidth  // autoFocus // type="email"
                           margin="dense" id="id_username" variant="filled"
                           name="username" label="User Name"
                />
                <br/>
                <TextField fullWidth
                           margin="dense" id="id_password" label="Password"
                           name="password" type="password" variant="filled"
                />
                <br/>
                <button id={"btnSubmit"} className={"btn btn-site"} type={"submit"} onClick={this.submitLogin}
                        variant="contained" style={{"margin": "10px"}}>
                    Submit
                </button>
                {/*</Grid>*/}
                {/*<Grid item xs={6} style={{"textAlign":"center"}}>*/}
                <button id={"btnCancel"} className={"btn btn-site"} onClick={this.props.handleCloseSignInForm}
                        variant="contained" style={{"margin": "10px"}}>
                    Cancel
                </button>

            </Container>

        )
    }
}

export default withStyles(styles)(SignInFormPage);
