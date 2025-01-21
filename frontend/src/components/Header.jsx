import "./Header.css";
import LoginButton from "./LoginPopup";

const Header = () => (
  <header>
    {/* 홈 버튼 */}
    <div className="header-left"></div>
    {/* 내비게이션 메뉴 */}

    <div className="header-center">
      <ul>
        <li>게시판</li>
        <li>학교정보</li>
        {/* 메뉴 추가 가능 */}
      </ul>
    </div>
    {/* 로그인 버튼 */}
    <div className="header-right">
      <LoginButton></LoginButton>
    </div>
  </header>
);

export default Header;
