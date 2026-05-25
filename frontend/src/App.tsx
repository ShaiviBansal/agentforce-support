import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Chat from "./pages/Chat";

const PrivateRoute = ({ children }: { children: JSX.Element }) => {
	const token = localStorage.getItem("token");
	return token ? children : <Navigate to="/" />;
};

const App = () => {
	return (
		<BrowserRouter>
			<Routes>
				<Route path="/" element={<Login />} />
				<Route
					path="/chat"
					element={
						<PrivateRoute>
							<Chat />
						</PrivateRoute>
					}
				/>
			</Routes>
		</BrowserRouter>
	);
};

export default App;
