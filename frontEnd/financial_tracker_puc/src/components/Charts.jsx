"use client";
import { useEffect, useState, useRef } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

export default function SpendingOverTimeChart() {
  const [debitData, setDebitData] = useState(null);
  const [creditData, setCreditData] = useState(null);
  const [error, setError] = useState(null);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const chartRef = useRef(null);

  useEffect(() => {
    const fetchBoth = async () => {
      try {
        const [debitRes, creditRes] = await Promise.all([
          fetch("/api/expenses_statistics"),
          fetch("/api/credits_statistics"),
        ]);
        const [debitText, creditText] = await Promise.all([
          debitRes.text(),
          creditRes.text(),
        ]);

        setDebitData(JSON.parse(debitText));
        setCreditData(JSON.parse(creditText));
      } catch (err) {
        console.error("❌ Error fetching data:", err);
        setError("Failed to load data");
      }
    };

    fetchBoth();
  }, []);

  const filteredDebits = Array.isArray(debitData)
    ? debitData.filter((d) => {
        const date = new Date(`${d.month}-01`);
        return (!startDate || date >= startDate) && (!endDate || date <= endDate);
      })
    : [];

  const filteredCredits = Array.isArray(creditData)
    ? creditData.filter((d) => {
        const date = new Date(`${d.month}-01`);
        return (!startDate || date >= startDate) && (!endDate || date <= endDate);
      })
    : [];

  const months = [...new Set([...filteredDebits, ...filteredCredits].map((d) => d.month))].sort();
  const categories = [...new Set(filteredDebits.map((d) => d.category))];

  const datasets = [];

  categories.forEach((category) => {
    const categoryData = months.map((month) => {
      const match = filteredDebits.find((d) => d.category === category && d.month === month);
      return match ? match.total : 0;
    });

    datasets.push({
      label: category,
      data: categoryData,
      borderColor: stringToColor(category),
      backgroundColor: stringToColor(category),
      tension: 0.3,
      fill: false,
    });
  });

  const debitTotals = months.map((month) =>
    filteredDebits.filter((d) => d.month === month).reduce((sum, d) => sum + d.total, 0)
  );
  datasets.push({
    label: "Total Expenses",
    data: debitTotals,
    borderColor: "rgba(255, 99, 132, 1)",
    backgroundColor: "rgba(255, 99, 132, 0.2)",
    borderDash: [4, 4],
    borderWidth: 2,
    tension: 0.3,
    fill: false,
  });

  const creditTotals = months.map((month) =>
    filteredCredits.filter((d) => d.month === month).reduce((sum, d) => sum + d.total, 0)
  );
  datasets.push({
    label: "Total Credits",
    data: creditTotals,
    borderColor: "rgba(59, 130, 246, 1)",
    backgroundColor: "rgba(59, 130, 246, 0.2)",
    borderWidth: 2,
    tension: 0.3,
    fill: false,
  });

  const chartData = {
    labels: months,
    datasets,
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        onClick: (e, legendItem, legend) => {
          const nativeEvent = e.native;
          const chart = legend.chart;
          const index = legendItem.datasetIndex;
          const isVisible = chart.isDatasetVisible(index);

          const isModifierPressed =
            nativeEvent?.ctrlKey || nativeEvent?.metaKey || nativeEvent?.shiftKey;

          if (isModifierPressed) {
            chart.setDatasetVisibility(index, !isVisible);
          } else {
            const onlyThisVisible = chart.data.datasets.every((_, i) =>
              i === index ? isVisible : !chart.isDatasetVisible(i)
            );
            chart.data.datasets.forEach((_, i) => {
              chart.setDatasetVisibility(i, onlyThisVisible || i === index);
            });
          }

          chart.update();
        },
      },
    },
  };

  useEffect(() => {
    if (!chartRef.current) return;
    const chart = chartRef.current;

    if (!debitData || !creditData || !chart.data) return;

    chart.data.datasets?.forEach((ds, i) => {
      if (ds.label !== "Total Expenses" && ds.label !== "Total Credits") {
        chart.setDatasetVisibility(i, false);
      }
    });
    chart.update();
  }, [debitData, creditData]);

  if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;
  if (!Array.isArray(debitData) || !Array.isArray(creditData))
    return <p className="text-center mt-10 text-gray-500">Loading chart...</p>;

  return (
    <div className="max-w-4xl mx-auto mt-10 bg-white p-4 rounded shadow">
      <h2 className="text-xl font-semibold text-center mb-4 text-gray-600">Spending and Credits Over Time</h2>

      <div className="flex flex-wrap justify-center gap-4 mb-6">
        <DatePicker
          selected={startDate}
          onChange={(date) => setStartDate(date)}
          selectsStart
          startDate={startDate}
          endDate={endDate}
          placeholderText="Start date"
          className="px-2 py-1 border rounded text-gray-900"
        />
        <DatePicker
          selected={endDate}
          onChange={(date) => setEndDate(date)}
          selectsEnd
          startDate={startDate}
          endDate={endDate}
          minDate={startDate}
          placeholderText="End date"
          className="px-2 py-1 border rounded text-gray-900"
        />
      </div>

      <Line ref={chartRef} data={chartData} options={options} />
    </div>
  );
}

function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash);
  }
  return `hsl(${hash % 360}, 70%, 60%)`;
}