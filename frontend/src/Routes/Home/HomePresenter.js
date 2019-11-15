import React from "react";
import PropTypes from "prop-types";
import styled from "styled-components";
import Helmet from "react-helmet";
import Loader from "Components/Loader";

const Container = styled.div`
    padding: 20px;
`;

const HomePresenter = ({ error, loading }) => (
    <>
        <Helmet>
            <title>Main | 1 Day 1 Commit</title>
        </Helmet>
        {loading ? (
            <Loader />
        ) : (
            <Container>
                <h1>Hello World!</h1>
            </Container>
        )}
    </>
);

HomePresenter.propTypes = {
    error: PropTypes.string,
    loading: PropTypes.bool.isRequired
};

export default HomePresenter;
