import { useEffect, useState } from "react";

const API = "http://localhost:8000"

function App() {

  const [users, setUsers] = useState([])
  const [tasks, setTasks] = useState([])

  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [taskName, setTaskName] = useState("")
  const [taskDescription, setTaskDescription] = useState("")
  const [priority, setPriority] = useState("medium")
  const [dueDate, setTaskDueDate] = useState("")
  const [userId, setUserId] = useState("")

  useEffect(() => {
    getUsers()
    getTasks()
  }, [])

  async function getUsers(){
    const res = await fetch(`${API}/users/`)
    const data = await res.json()
    setUsers(data)
  }

  async function getTasks(){
    const res = await fetch(`${API}/tasks/`)
    const data = await res.json()
    setTasks(data)
  }

  async function createUser(e){
    e.preventDefault()

    await fetch(`${API}/users/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: name,
        email: email,
        password: password
      })
    })

    setName("")
    setEmail("")
    setPassword("")
    await getUsers()
  }

  async function deleteUser(Id) {
    await fetch(`${API}/users/${Id}`,{
      method: "DELETE",
    })

    await getUsers()
    await getTasks()
  }

  async function createTask(e) {
    e.preventDefault()

    await fetch(`${API}/tasks/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: taskName,
        description: taskDescription,
        completed: false,
        priority: priority,
        due_date: dueDate,
        user_id: userId
      })
    })

    setTaskName("")
    setTaskDescription("")
    setPriority("medium")
    setTaskDueDate("")
    setUserId("")

    await getTasks()
  }

  async function updateTask(task){
    await fetch(`${API}/tasks/${task.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json" 
      },
      body: JSON.stringify({
        name: task.name,
        description: task.description,
        completed: !task.completed,
        priority: task.priority,
        due_date: task.due_date,
        user_id: task.user_id
      })
    })

    await getTasks()

  }

  async function deleteTask(id){
    await fetch (`${API}/tasks/${id}`,{
      method : "DELETE"
    })

    await getTasks()
  }


  return (
    <div>
      <h1>Task Management App</h1>

      {/* Users */}
      <h2>Create User</h2>
      <form onSubmit={createUser}>
          <input
            placeholder="Name"
            value={name}
            onChange={(e) => {setName(e.target.value)}}
          />
          <input
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        <button type="submit">Create User</button>
      </form>
      <h2>Users</h2>

      <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Email</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
        {users.map((user) => (
         <tr key={user.id}>
          <td>{user.id}</td>
          <td>{user.name}</td>
          <td>{user.email}</td>
          <td>{user.created_at}</td>
          <td>{user.updated_at}</td>
          <td>
          <button onClick={() => deleteUser(user.id)}>Delete</button>
          </td>
        </tr>
        ))}
        </tbody>
      </table>

      <hr/>
      {/* Tasks */}
      <h2>Create Task</h2>

      <form onSubmit={createTask}>
        <input
        placeholder="name"
        value={taskName}
        onChange={(e) => setTaskName(e.target.value)}
        />
        <input
        placeholder="description"
        value={taskDescription}
        onChange={(e) => setTaskDescription(e.target.value)}
        />
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="low">low</option>
          <option value="medium">medium</option>
          <option value="high">high</option>
        </select>
        
        <input
        placeholder="Due Date"
        value={dueDate}
        onChange={(e) => setTaskDueDate(e.target.value)}
        />

        <label>Select User</label>
        <select value={userId} onChange={(e) => setUserId(e.target.value)}>
        <option value="">Select User</option>


          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
        </select>

        <button type="submit">Create Task</button>
      </form>
      
      <h2>Tasks</h2>
      <table>
        <thead>
          <tr>
            <th>Id</th>
            <th>Name</th>
            <th>Description</th>
            <th>Completed</th>
            <th>Priority</th>
            <th>Due Date</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th>User Id</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
        {tasks.map((task) => (
          <tr key={task.id}>
           <td>{task.id}</td>
           <td>{task.name}</td>
           <td>{task.description}</td>
           <td>{task.completed ? "Yes" : "No"}</td>
           <td>{task.priority}</td>
           <td>{task.due_date}</td>
           <td>{task.created_at}</td>
           <td>{task.updated_at}</td>
           <td>{task.user_id}</td>
           <td>
            <button onClick={() => updateTask(task)}>Update</button>
           </td>
           <td>
            <button onClick={() => deleteTask(task.id)}>Delete</button>
           </td>
         </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;