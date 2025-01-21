import Header from "./components/Header";
import MainBody from "./components/MainBody";
import Footer from "./components/Footer";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import SignupPage from "./pages/SignupPage"; // SignupPage 가져오기

const App = () => {
  return (
    <Router>
      <div className="app-container">
        {/* SignupPage 경로일 때 Header를 렌더링하지 않음 */}
        <Routes>
          <Route
            path="/signup"
            element={
              <>
                <SignupPage />
              </>
            }
          />
          <Route
            path="/"
            element={
              <>
                <Header /> {/* MainBody가 있는 페이지에서는 Header 표시 */}
                <MainBody />
              </>
            }
          />
        </Routes>
        <Footer />
      </div>
    </Router>
  );
};

export default App;
