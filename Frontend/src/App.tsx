import { CreatePage } from "./Pages/CreatePage"
import { LoginPage } from "./Pages/LoginPage"
import {Routes,Route} from "react-router-dom"
function App() {
  return (
    <div>
      <Routes>
        <Route path="/create" element={<CreatePage/>}></Route>
        <Route path="/login" element={<LoginPage/>}></Route>
      </Routes>

    </div>
  )
}

export default App
