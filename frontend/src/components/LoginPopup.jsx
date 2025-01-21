import { useState } from "react";
import PropTypes from "prop-types"; // PropTypes import
import "./Login.css";
import { login } from "../services/authService"; // login 함수 import
import { useNavigate } from "react-router-dom"; // useNavigate import

// 로그인 팝업 내용
const LoginPopup = ({ isOpen, onClose }) => {
  const [username, setUsername] = useState(""); // 사용자 이름 상태
  const [password, setPassword] = useState(""); // 비밀번호 상태
  const [error, setError] = useState(null); // 에러 메시지 상태

  const navigate = useNavigate();

  if (!isOpen) return null;

  // 로그인 버튼 클릭 핸들러
  const handleLogin = async () => {
    try {
      const response = await login(username, password); // API 호출
      console.log("로그인 성공:", response);
      alert("로그인 성공!");
      onClose(); // 팝업 닫기
    } catch (err) {
      console.error("로그인 실패:", err);
      setError("로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.");
    }
  };

  const handleSignupClick = () => {
    onClose();
    navigate("/signup");
  };

  return (
    <div className="popup-overlay">
      <div className="popup">
        <button className="close-button" onClick={onClose}>
          X
        </button>
        <h2>Login</h2>
        {error && <p className="error-message">{error}</p>}{" "}
        {/* 에러 메시지 표시 */}
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)} // 입력 값 업데이트
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)} // 입력 값 업데이트
        />
        <button className="login-button" onClick={handleLogin}>
          로그인
        </button>
        <button className="signup-button" onClick={handleSignupClick}>
          회원가입
        </button>
      </div>
    </div>
  );
};

// PropTypes 정의
LoginPopup.propTypes = {
  isOpen: PropTypes.bool.isRequired, // isOpen은 boolean이며 필수
  onClose: PropTypes.func.isRequired, // onClose는 함수이며 필수
};

const LoginButton = () => {
  const [isPopupOpen, setPopupOpen] = useState(false);

  const handleLoginClick = () => {
    setPopupOpen(true);
  };
  const handleClosePopup = () => {
    setPopupOpen(false);
  };

  return (
    <div>
      <button className="main-login-button" onClick={handleLoginClick}>
        로그인
      </button>
      <LoginPopup isOpen={isPopupOpen} onClose={handleClosePopup}></LoginPopup>
    </div>
  );
};

export default LoginButton;
