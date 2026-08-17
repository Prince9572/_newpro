import React from "react";
import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "../utils/firebase";

function App() {
  const googleLogin = async () => {
    console.log(auth);
    console.log(googleProvider);
  
    try {
      const result = await signInWithPopup(auth, googleProvider);
  
      console.log("User:", result.user);
      console.log("Credential:", result);
    } catch (error) {
      console.error("Code:", error.code);
      console.error("Message:", error.message);
      console.error(error);
    }
  };

  return (
    <div className="w-screen h-screen bg-gray-900 flex items-center justify-center">
      <button
        className="w-50 h-24 bg-white"
        onClick={googleLogin}
      >
        Click
      </button>
    </div>
  );
}

export default App;