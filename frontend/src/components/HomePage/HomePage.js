import React, { useState } from "react";
import { Link } from 'react-router-dom';
import UsersDetailsPage from "../UsersDetailsPage/UsersDetailsPage";


const LinkItem = ({ to, children }) => {
  const [hover, setHover] = useState(false);

  const linkStyle = {
    textDecoration: 'none',
    color: hover ? '#0056b3' : 'black',
    backgroundColor: hover ? '#e8f0fe' : 'transparent',
    padding: '10px',
    borderRadius: '5px',
    display: 'block', // Расширяет кликабельную область
    cursor: 'pointer'
  };

  return (
    <li style={{ marginBottom: '5px', fontSize: '16px' }}>
      <Link
        to={to}
        style={linkStyle}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
      >
        {children}
      </Link>
    </li>
  );
};
const links = [
    { path: '/registration', label: 'Registration' },
    { path: '/logIn', label: 'Log In' },
    { path: '/activate/:token', label: 'Activate Account (open from email follow link)' },
    { path: '/profile', label: 'User Profile (if you have one)' },
    { path: '/addavatar', label: 'Add Avatar' },
    { path: '/upgradeaccount', label: 'Upgrade Account $' },
    { path: "/recoverpassword", label: 'New password request' },
    { path: "/recovery/:token", label: 'Reset password (open from email' },
    { path: '/deleteaccount', label: 'Delete Account' },
    { path: '/logout', label: 'Log Out' },


    { path: '', label: '' },

    { path: '/createmanager', label: 'Create Manager (for superuser)' },
    { path: '/addblacklist', label: 'Add to Blacklist (for manager)' },
    { path: '/removeblacklist', label: 'Remove from Blacklist (for manager)' },


    { path: '', label: '' },

    { path: '/listingcreate', label: 'Create Listing (for sellers)' },
    { path: '/listingsuserlist', label: "User's Listings List" },
    { path: '/listings/update/:id', label: 'Update Listing (open from Users listings list)' },
    { path: '/listingsuserdetails/:id', label: "Listing Detail (open page from User\'s Listings)" },
    { path: '/delete/:id', label: "Delete Listing (open page from User\'s Listings)" },
    { path: '/list', label: 'All Car Listings' },
    { path: '/alllistingsdetails/:id', label: 'Car Listing Details including stats for premium sellers (open page from All Car Listings)' },
    { path: '/listingsearch', label: 'Search listings with filters' },
];

const HomePage = () => {
    return (
    <div style={{
      position: 'relative',
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      padding: '20px',
      backgroundColor: '#f4f4f4'
    }}>
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%'
      }}>
        <div style={{ textAlign: 'left' }}>
          <h2>Welcome to Car Sales!</h2>
        </div>
        <div style={{ textAlign: 'right' }}>
          <UsersDetailsPage />
        </div>
      </div>

          <nav style={{ marginTop: '20px' }}>
        <ul style={{
          listStyleType: 'none',
          padding: 0,
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
          backgroundColor: '#fff',
          boxShadow: '0 2px 5px rgba(0, 0, 0, 0.1)',
          borderRadius: '5px',
          overflow: 'auto'
        }}>
          {links.map(({ path, label }) => (
            <LinkItem to={path} key={path}>{label}</LinkItem>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default HomePage;

