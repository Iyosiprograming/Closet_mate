import { NotFoundPage } from "./Pages/NotFoundPage"
import { MainPage } from "./Pages/MainPage"
import { RegisterPage } from "./Pages/RegisterPage"
import {Route,Routes} from "react-router-dom"
function App() {

  return (
    <>
      <Routes>
        <Route path="/register" element={<RegisterPage />} />
        <Route path="*" element={<NotFoundPage />} />
        <Route path="/" element={<MainPage />} />
      </Routes>
    </>
  )
}

export default App
