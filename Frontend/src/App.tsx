import { NotFoundPage } from "./Pages/NotFoundPage"
import { MainPage } from "./Pages/MainPage"
import {Route,Routes} from "react-router-dom"
function App() {

  return (
    <>
      <Routes>
        <Route path="*" element={<NotFoundPage />} />
        <Route path="/" element={<MainPage />} />
      </Routes>
    </>
  )
}

export default App
