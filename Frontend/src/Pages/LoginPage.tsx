import { useState } from "react"
import { LoginUser } from "../Services/UserApi"

export const LoginPage = () => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

const handelLogin = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault()

  try {
    const response = await LoginUser(email, password)

    console.log(response.message)
    alert(response.message)

  } catch (error) {
    console.error("Error creating account:", error)
    alert("Something went wrong")
  }
}

  return (
    <div>
      <form onSubmit={handelLogin}>
        <label>Email:</label>
        <input
          type="email"
          required
          placeholder="Enter Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Password:</label>
        <input
          type="password"
          required
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <input type="submit" value="Login" />
      </form>
    </div>
  )
}