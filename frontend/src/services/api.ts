import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

const api = axios.create({
	baseURL: BASE_URL,
});

// Attach JWT token to every request automatically
api.interceptors.request.use((config) => {
	const token = localStorage.getItem("token");
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

export const login = async (
	username: string,
	password: string,
): Promise<string> => {
	const formData = new URLSearchParams();
	formData.append("username", username);
	formData.append("password", password);

	const response = await api.post("/token", formData, {
		headers: { "Content-Type": "application/x-www-form-urlencoded" },
	});

	return response.data.access_token;
};

export const sendMessage = async (
	message: string,
): Promise<{ response: string; sources: string[] }> => {
	const response = await api.post("/chat", { message });
	return response.data;
};

export default api;
