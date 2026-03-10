import axios from "axios";

const BASE_URL = import.meta.env.VITE_API_URL;

interface RegisterResponse {
  status_code : number,
  message : string,
  detail: object
}

export const RegisterUser = async (email: string,password: string) => {
  const response = await axios.post<RegisterResponse>(
    `${BASE_URL}/users`,
    { email, password }
  );
  return response.data; 
};