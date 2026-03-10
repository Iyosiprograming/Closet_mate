import { useState } from "react";
import { RegisterUser } from "../Services/Api";

export const RegisterPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const response = await RegisterUser(email, password);
      alert(response.message);
    } catch (error:any) {
      alert(error.response?.data?.detail||"An error occurred during registration.");
    }
  };

  return (
    <div>
      <form onSubmit={handleRegister}>
        <label>Email:</label>
        <input
          type="email"
          required
          placeholder="Enter Email Here"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Password:</label>
        <input
          type="password"
          required
          placeholder="Enter Password Here"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input type="submit" value="Register" />
      </form>
    </div>
  );
};