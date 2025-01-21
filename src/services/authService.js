const API_URL = "https://example.com/api"; // 백엔드 API URL

/**
 * 로그인 API 호출
 * @param {string} username - 사용자 아이디
 * @param {string} password - 사용자 비밀번호
 * @returns {Promise<object>} - API 응답 데이터
 * @throws {Error} - 로그인 실패 시 에러
 */
export const login = async (username, password) => {
  try {
    // fetch 로 구현
    const response = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("로그인 실패: " + response.statusText);
    }

    const data = await response.json();
    return data; // 성공한 응답 데이터 반환
  } catch (error) {
    console.error("로그인 에러:", error);
    throw error; // 에러를 상위 호출자로 전달
  }
};
