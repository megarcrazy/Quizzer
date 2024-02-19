
import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';


const StyledNav = styled.nav`
    position: fixed;
    top: 0;
    width: 100%;
    background: #a1a1a1;
    padding: 10px;
    color: white;
`;

const StyledUl = styled.ul`
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
`;

const StyledLi = styled.li`
    display: inline;
    margin-left: 40px;
    margin-right: 10px;
`;

const StyledLink = styled(Link)`
    color: black;
    text-decoration: none;

    &:hover {
        text-decoration: underline;
    }
    &:visited {
        color: black;
    }
`;


/**
 * NavigationBar allows the user to easily browse across pages.
 * It is fixed at the top of each page of the website.
 * 
 * @returns {JSX.Element}
 */
const NavigationBar: React.FC = (): JSX.Element => {
    return (
        <StyledNav>
            <StyledUl>
                <StyledLi>
                    <StyledLink to="/home">Home</StyledLink>
                </StyledLi>
                <StyledLi>
                    <StyledLink to="/about">About</StyledLink>
                </StyledLi>
            </StyledUl>
        </StyledNav>
    );
};

export default NavigationBar;
