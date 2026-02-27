import axios from "axios";

const BaseUrl = "http://127.0.0.1:8000";

export const CreateAccount = async (email: string, password: string) => {
    try {
        const response = await axios.post(`${BaseUrl}/users/create`, { email, password });
        return response.data
    } catch (error) {
        console.error(error);
    }
}

export const LoginUser = async (email: string, password: string) => {
    try {
        const response = await axios.post(`${BaseUrl}/users/login`, { email, password },{withCredentials: true});
        return response.data
    } catch (error) {
        console.error(error);
    }
}