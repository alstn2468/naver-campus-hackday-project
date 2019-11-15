import React from "react";
import {
    HashRouter as Router,
    Route,
    Redirect,
    Switch
} from "react-router-dom";
import Home from "Routes/Home";
import Header from "Components/Header";

export default () => (
    <Router>
        <Header />
        <Switch>
            <Route path="/" exact component={Home} />
            <Redirect from="*" to="/" />
        </Switch>
    </Router>
);
