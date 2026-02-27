import { useState } from "react"
import { CreateAccount } from "../Services/UserApi"

export const CreatePage = () => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault()

  try {
    const response = await CreateAccount(email, password)

    console.log(response.message)
    alert(response.message)

  } catch (error) {
    console.error("Error creating account:", error)
    alert("Something went wrong")
  }
}

  return (
    <div>
      <form onSubmit={handleCreate}>
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

        <input type="submit" value="Create Account" />
      </form>
    </div>
  )
}