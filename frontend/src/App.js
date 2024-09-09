import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

import './AxiosConfig';
import LogIn from './components/LogIn/LogIn';
import HomePage from './components/HomePage/HomePage';
import ActivateAccount from './components/ActivateAccount/ActivateAccount';
import UsersProfile from "./components/UsersProfile/UsersProfile";
import RemoveFromBlackList from "./components/RemoveFromBlackList/RemoveFromBlackList";
import AddToBlacklist from "./components/AddToBlackList/AddToBlacklist";
import AddAvatar from "./components/AddAvatar/AddAvatar";
import CreateManager from "./components/CreateManager/CreateManager";
import UpgradeAccount from "./components/UpgradeAccount/UpgradeAccount";
import DeleteAccount from "./components/DeleteAccount/DeleteAccount";
import LogOut from "./components/LogOut/LogOut";
import ListingCreate from "./components/ListingCreate/ListingCreate";
import UpdateListingPage from "./components/UpdateListingPage/UpdateListingPage";
import ListingsUserList from "./components/ListingsUserList/ListingsUserList";
import ListingUselListDetail from "./components/ListingUserListDetail/ListingUserListDetail";
import AllListingsListDetails from "./components/AllListingsListDetails/AllListingsListDetails";
import AllListingsList from "./components/AllListingsList/AllListingsList";
import DeleteListingPage from "./components/ListingsDeletion/ListingsDeletion";
import RegistrationPage from "./components/RegistrationPage/RegistrationPage";
import PasswordRecoveryRequest from "./components/PasswordRecoveryRequest/PasswordRecoveryRequest";
import PasswordReset from "./components/PasswordReset/PasswordReset";
import ChatPage from "./components/ChatPage/ChatPage";
import ListingSearch from "./components/ListingSearch/ListingSearch";




export const App = () => {
    return (
        <Router>
            <Routes>
                 <Route path="/" element={<HomePage />} />
                 <Route path="/logIn" element={<LogIn />} />
                 <Route path="/activate/:token" element={<ActivateAccount />} />
                 <Route path="/profile" element={<UsersProfile />} />
                 <Route path="/addblacklist" element={<AddToBlacklist />} />
                 <Route path="/removeblacklist" element={<RemoveFromBlackList />} />
                 <Route path="/addavatar" element={<AddAvatar />} />
                 <Route path="/recoverpassword" element={<PasswordRecoveryRequest/>} />
                 <Route path="/recovery/:token" element={<PasswordReset/>} />
                 <Route path="/createmanager" element={<CreateManager />} />
                 <Route path="/upgradeaccount" element={<UpgradeAccount />} />
                 <Route path="/deleteaccount" element={<DeleteAccount />} />
                 <Route path="/logout" element={<LogOut />} />
                 <Route path="/listingcreate" element={<ListingCreate />} />
                 <Route path="/listingsuserlist" element={<ListingsUserList />} />
                 <Route path="/listings/update/:id" element={<UpdateListingPage />} />
                 <Route path="/listingsuserdetails/:id" element={<ListingUselListDetail />} />
                 <Route path="/list" element={<AllListingsList />} />
                 <Route path="/alllistingsdetails/:id" element={<AllListingsListDetails />} />
                 <Route path="/delete/:id" element={<DeleteListingPage />} />
                 <Route path="/registration" element={<RegistrationPage />} />
                <Route path="/chat/:listingId" element={<ChatPage />} />
                <Route path="/listingsearch" element={<ListingSearch />} />
            </Routes>
        </Router>
    );
};

export default App;

