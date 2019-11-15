import React from "react";
import { Link, withRouter } from "react-router-dom";
import styled from "styled-components";
import { CLIENT_ID, REDIRECT_URI } from "Components/Config";

const Header = styled.header`
    color: white;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 50px;
    display: flex;
    align-items: center;
    padding: 0px 10px;
    background-color: #000000;
    z-index: 10;
    box-shadow: 0px 1px 3px 2px rgba(0, 0, 0, 0.2);
`;

const List = styled.ul`
    display: flex;
    flex: 8;
`;

const Item = styled.li`
    width: 100px;
    height: 50px;
    text-align: center;
    border-bottom: 3px solid
        ${props => (props.current ? "#AA00FF" : "transparent")};
    transition: border-bottom 0.5s ease-in-out;
`;

const SLink = styled(Link)`
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 500;
    color: #ffffff;
`;

const UserStatus = styled.a`
    height: 50px;
    display: flex;
    flex: 2;
    align-items: center;
    justify-content: flex-end;
    font-size: 12px;
    font-weight: 400;
    padding-right: 40px;
    text-align: right;
    color: #ffffff;
`;

export default withRouter(({ location: { pathname } }) => (
    <Header>
        <List>
            <Item current={pathname === "/"}>
                <SLink to="/">Main</SLink>
            </Item>
        </List>
        <UserStatus
            href={`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID}&scope=user&redirect_uri=${REDIRECT_URI}`}
        >
            Github로 Login
        </UserStatus>
    </Header>
));
