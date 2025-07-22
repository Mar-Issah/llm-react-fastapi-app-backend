import './App.css';
import { Routes, Route } from 'react-router-dom';
import AuthenticationPage from './auth/AuthenticationPage';
import Layout from './layout/Layout';
import ClerkProviderWrapper from './auth/ClerkProviderWrapper';
import ChallengeGenerator from './components/ChallengeGenerator';
import ChallengeHistory from './components/ChallengeHistory';

function App() {
  return (
    <ClerkProviderWrapper>
      <Routes>
        {/* the * means that the path can have any additional segments after '/sign-in' */}
        <Route path='/sign-in/*' element={<AuthenticationPage />} />
        <Route path='/sign-up' element={<AuthenticationPage />} />
        <Route element={<Layout />}>
          <Route path='/' element={<ChallengeGenerator />} />
          <Route path='/history' element={<ChallengeHistory />} />
        </Route>
      </Routes>
    </ClerkProviderWrapper>
  );
}

export default App;
