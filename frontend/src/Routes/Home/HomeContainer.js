import React from "react";
import HomePresenter from "./HomePresenter";

export default class extends React.Component {
    state = {
        error: null,
        loading: false
    };

    componentDidMount() {}

    render() {
        const { error, loading } = this.state;

        return <HomePresenter error={error} loading={loading} />;
    }
}
