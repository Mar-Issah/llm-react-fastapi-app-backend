import 'react';
import { SignedIn, SignedOut, UserButton } from '@clerk/clerk-react';
import { Outlet, Link, Navigate } from 'react-router-dom';

const Layout = () => {
  return (
    <div className='main-layout'>
      <header className='main-header'>
        <div className='main-header-content'>
          <p className='main-title'>Challenge Generator</p>
          <nav className='main-nav'>
            <SignedIn>
              <Link className='main-nav-link' to='/'>
                Generate Challenge
              </Link>
              <Link className='main-nav-link' to='/history'>
                History
              </Link>
              <UserButton />
            </SignedIn>
          </nav>
        </div>
      </header>

      <main className='main-content'>
        <SignedOut>
          <Navigate to='/sign-in' replace />
        </SignedOut>
        <SignedIn>
          <Outlet />
        </SignedIn>
      </main>
    </div>
  );
};

export default Layout;
