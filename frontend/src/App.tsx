import { useState, useEffect } from "react";
import axios from "axios";
import { PieChart, Pie, Cell, Tooltip } from "recharts";

interface ActivityRow {
  timestamp: string;
  app: string;
  detail: string;
  duration: number;
}

interface ChartData {
  name: string;
  value: number;
}

export default function App() {
  const [data, setData] = useState<ActivityRow[]>([]);
  const [summary, setSummary] = useState<string>("");
  const [multiSummary, setMultiSummary] = useState<string>("");

  const fetchData = async () => {
    const res = await axios.get<{ data: ActivityRow[] }>("http://localhost:8000/data");
    setData(res.data.data);
  };

  const summariseDay = async () => {
    const res = await axios.get<{ summary: string }>("http://localhost:8000/summary");
    setSummary(res.data.summary);
  };

  const summariseMulti = async () => {
    const res = await axios.get<{ summary: string }>("http://localhost:8000/summary/multi?last_n=7");
    setMultiSummary(res.data.summary);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const grouped = data.reduce<Record<string, number>>((acc, row) => {
    acc[row.app] = (acc[row.app] || 0) + row.duration;
    return acc;
  }, {});

  const chartData: ChartData[] = Object.entries(grouped).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-4">Day Summariser</h1>

      <div className="space-x-4">
        <button onClick={summariseDay} className="bg-blue-500 text-white px-4 py-2 rounded">
          Summarise Today
        </button>
        <button onClick={summariseMulti} className="bg-green-500 text-white px-4 py-2 rounded">
          Summarise Last 7 Days
        </button>
      </div>

      {summary && <p className="mt-4"><b>Today:</b> {summary}</p>}
      {multiSummary && <p className="mt-4"><b>Last 7 Days:</b> {multiSummary}</p>}

      <PieChart width={400} height={400}>
        <Pie data={chartData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={150}>
          {chartData.map((_, idx) => (
            <Cell key={idx} fill={`hsl(${idx * 40},70%,50%)`} />
          ))}
        </Pie>
        <Tooltip />
      </PieChart>
    </div>
  );
}
