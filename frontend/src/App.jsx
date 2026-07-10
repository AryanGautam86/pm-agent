import { useEffect, useState } from "react";
// const API = import.meta.env.VITE_API_URL;
const API = "";
function App() {
  const [message, setMessage] = useState("");
  const [reply, setReply] = useState("");
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const totalProjects = projects.length;
  const totalTasks = tasks.length;
  const completedTasksOverall = tasks.filter(
    (task) => task.status === "Done").length;
  const overallProgress =
    totalTasks === 0
      ? 0
      : Math.round((completedTasksOverall / totalTasks) * 100);


  async function loadProjects() {
    const res = await fetch(`${API}/projects`);
    const data = await res.json();
    setProjects(data);
  }

  async function loadTasks() {
    const res = await fetch(`${API}/tasks`);
    const data = await res.json();
    setTasks(data);
  }

  useEffect(() => {
    loadProjects();
    loadTasks();
  }, []);

  async function sendMessage() {
    if (!message.trim()) return;

    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();

    // Beautiful AI responses
    if (data.project) {
      setReply(`🎉 Project "${data.project.name}" created successfully.`);
    } else if (data.message) {
      if (data.message.includes("Project created")) {
        setReply(`🎉 ${data.message}`);
      } else if (data.message.includes("Task created")) {
        setReply(`✅ ${data.message}`);
      } else if (data.message.includes("Task marked")) {
        setReply(`🟢 ${data.message}`);
      } else if (data.message.includes("Task deleted")) {
        setReply(`🗑️ ${data.message}`);
      } else if (data.message.includes("Project deleted")) {
        setReply(`🗂️ ${data.message}`);
      } else if (data.message.includes("already exists")) {
        setReply(`⚠️ ${data.message}`);
      } else {
        setReply(data.message);
      }
    } else if (data.reply) {
      setReply(`🤖 ${data.reply}`);
    } else {
      setReply(JSON.stringify(data, null, 2));
    }

    await loadProjects();
    await loadTasks();

    setMessage("");
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex justify-center py-12">
      <div className="w-full max-w-5xl">

        {/* Header */}
        <h1 className="text-5xl font-bold text-center mb-10">
          🤖 PM Agent
        </h1>

        {/* Input */}
        <div className="flex gap-3 mb-8">
          <input
            className="flex-1 rounded-lg bg-gray-800 px-4 py-3 outline-none border border-gray-700"
            placeholder="Type something like 'Create project AI Chatbot'..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") sendMessage();
            }}
          />

          <button
            onClick={sendMessage}
            className="bg-blue-600 hover:bg-blue-700 transition px-6 rounded-lg font-semibold"
          >
            Send
          </button>
        </div>
        {/* Dashboard Summary */}

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">

          <div className="bg-gray-900 rounded-xl p-5 text-center shadow-lg">
            <h3 className="text-gray-400 text-sm">Projects</h3>
            <p className="text-3xl font-bold text-blue-400">
              {totalProjects}
            </p>
          </div>

          <div className="bg-gray-900 rounded-xl p-5 text-center shadow-lg">
            <h3 className="text-gray-400 text-sm">Tasks</h3>
            <p className="text-3xl font-bold text-yellow-400">
              {totalTasks}
            </p>
          </div>

          <div className="bg-gray-900 rounded-xl p-5 text-center shadow-lg">
            <h3 className="text-gray-400 text-sm">Completed</h3>
            <p className="text-3xl font-bold text-green-400">
              {completedTasksOverall}
            </p>
          </div>

          <div className="bg-gray-900 rounded-xl p-5 text-center shadow-lg">
            <h3 className="text-gray-400 text-sm">Overall Progress</h3>
            <p className="text-3xl font-bold text-purple-400">
              {overallProgress}%
            </p>
          </div>

        </div>

        {/* Main Grid */}
        <div className="grid md:grid-cols-2 gap-8">

          {/* AI Response */}
          <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">
              💬 AI Response
            </h2>

            <div className="text-green-400 text-lg whitespace-pre-wrap leading-8">
              {reply || "🤖 No response yet"}
            </div>
          </div>

          {/* Projects */}
          <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
            <h2 className="text-2xl font-semibold mb-4">
              📁 Projects
            </h2>

            {projects.length === 0 ? (
              <p className="text-gray-400">
                No projects found.
              </p>
            ) : (
              <div className="space-y-4">

                {projects.map((project) => {

                  const projectTasks = tasks.filter(
                    (task) => task.project_id === project.id
                  );

                  const completedTasks = projectTasks.filter(
                    (task) => task.status === "Done"
                  ).length;

                  const progress =
                    projectTasks.length === 0
                      ? 0
                      : Math.round(
                        (completedTasks / projectTasks.length) * 100
                      );

                  return (
                    <div
                      key={project.id}
                      className="bg-gray-800 rounded-xl p-4 border border-gray-700"
                    >

                      <h3 className="text-lg font-bold text-blue-400">
                        📁 {project.name}
                      </h3>

                      {/* Progress */}
                      <div className="mt-3 mb-4">

                        <div className="flex justify-between text-sm mb-2">
                          <span>
                            Progress: {completedTasks} / {projectTasks.length} Completed
                          </span>

                          <span className="font-semibold text-green-400">
                            {progress}%
                          </span>
                        </div>

                        <div className="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500 transition-all duration-500"
                            style={{
                              width: `${progress}%`,
                            }}
                          />
                        </div>

                      </div>

                      {/* Tasks */}
                      <div className="space-y-2">

                        {projectTasks.length === 0 ? (
                          <p className="text-gray-400 text-sm">
                            No tasks yet.
                          </p>
                        ) : (
                          projectTasks.map((task) => (
                            <div
                              key={task.id}
                              className="flex items-center justify-between bg-gray-700 rounded-lg px-4 py-3"
                            >
                              <div className="flex items-center gap-3">

                                <span className="text-xl">
                                  {task.status === "Done"
                                    ? "🟢"
                                    : task.status === "In Progress"
                                      ? "🔵"
                                      : "🟡"}
                                </span>

                                <div>
                                  <p className="font-medium">{task.title}</p>

                                  {/* Priority */}
                                  <div className="mt-1">
                                    {task.priority === "High" && (
                                      <span className="inline-block text-xs font-semibold bg-red-500/20 text-red-400 px-2 py-1 rounded-full">
                                        🔴 High
                                      </span>
                                    )}

                                    {task.priority === "Medium" && (
                                      <span className="inline-block text-xs font-semibold bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded-full">
                                        🟡 Medium
                                      </span>
                                    )}

                                    {task.priority === "Low" && (
                                      <span className="inline-block text-xs font-semibold bg-green-500/20 text-green-400 px-2 py-1 rounded-full">
                                        🟢 Low
                                      </span>
                                    )}
                                  </div>

                                  {/* Due Date */}
                                  {task.due_date && (
                                    <p className="text-xs text-gray-400 mt-1">
                                      📅 Due: {task.due_date}
                                    </p>
                                  )}
                                </div>

                              </div>

                              <span
                                className={`text-sm font-semibold ${task.status === "Done"
                                  ? "text-green-400"
                                  : task.status === "In Progress"
                                    ? "text-blue-400"
                                    : "text-yellow-400"
                                  }`}
                              >
                                {task.status}
                              </span>
                            </div>
                          ))
                        )}

                      </div>

                    </div>
                  );
                })}

              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}

export default App;