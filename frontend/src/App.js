import { useState } from "react";
import axios from "axios";
import {
  ComposedChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const API_BASE = "https://stock-sentiment-dashboard-production.up.railway.app";

const colors = {
  bg: "#F5F0E8",
  surface: "#EDE8DC",
  border: "#C8BEA8",
  text: "#1A1712",
  muted: "#5C4F3A",
  accent: "#8B4513",
  positive: "#2D5016",
  negative: "#8B1A1A",
  neutral: "#5C4A2A",
  price: "#8B4513",
  sentiment: "#2D5016",
};

const card = {
  background: colors.surface,
  border: `2px solid ${colors.border}`,
  borderRadius: "2px",
  padding: "24px",
};

export default function App() {
  const [ticker, setTicker] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [priceData, setPriceData] = useState([]);
  const [articles, setArticles] = useState([]);
  const [avgSentiment, setAvgSentiment] = useState(null);
  const [sentimentLabel, setSentimentLabel] = useState("");

  const handleSearch = async () => {
    if (!ticker) return;
    setLoading(true);
    setError(null);
    try {
      const [priceRes, sentimentRes] = await Promise.all([
        axios.get(`${API_BASE}/api/stock/${ticker}`),
        axios.get(`${API_BASE}/api/sentiment/${ticker}`),
      ]);
      setPriceData(priceRes.data.prices);
      setArticles(sentimentRes.data.articles);
      setAvgSentiment(sentimentRes.data.average_sentiment);
      const score = sentimentRes.data.average_sentiment;
      if (score > 0.2) setSentimentLabel("Positive");
      else if (score < -0.2) setSentimentLabel("Negative");
      else setSentimentLabel("Neutral");
    } catch (err) {
      setError("Something went wrong. Is the Flask server running?");
    }
    setLoading(false);
  };

  const getSentimentColor = (s) => {
    if (s === "positive" || s === "Positive") return colors.positive;
    if (s === "negative" || s === "Negative") return colors.negative;
    return colors.neutral;
  };

  const getBadgeStyle = (sentiment) => ({
    background: "transparent",
    border: `1px solid ${getSentimentColor(sentiment)}`,
    color: getSentimentColor(sentiment),
    padding: "2px 8px",
    borderRadius: "2px",
    fontSize: "11px",
    fontWeight: "600",
    whiteSpace: "nowrap",
    letterSpacing: "0.05em",
    textTransform: "uppercase",
    fontFamily: "'Courier New', monospace",
  });

  const chartData = priceData.map((p) => {
    const match = articles.find((a) => a.date === p.date);
    return {
      date: p.date.slice(5),
      price: parseFloat(p.close.toFixed(2)),
      sentiment: match ? match.score : 0,
    };
  });

  return (
    <div style={{
      minHeight: "100vh",
      background: colors.bg,
      color: colors.text,
      padding: "48px 40px",
      fontFamily: "'Inter', sans-serif",
    }}>
      <div style={{ maxWidth: "1100px", margin: "0 auto" }}>

        {/* Header */}
        <div style={{ marginBottom: "40px", borderBottom: `3px solid ${colors.text}`, paddingBottom: "24px" }}>
          <p style={{
            color: colors.muted,
            fontSize: "11px",
            fontWeight: "600",
            letterSpacing: "0.2em",
            textTransform: "uppercase",
            margin: "0 0 10px 0",
            fontFamily: "'Courier New', monospace",
          }}>
            Market Intelligence / Sentiment Analysis
          </p>
          <h1 style={{
            fontSize: "42px",
            fontWeight: "700",
            margin: "0 0 8px 0",
            color: colors.text,
            letterSpacing: "-1px",
            fontFamily: "Georgia, 'Times New Roman', serif",
            lineHeight: 1.1,
          }}>
            Stock Sentiment Dashboard
          </h1>
          <p style={{ color: colors.muted, margin: 0, fontSize: "14px", fontFamily: "'Courier New', monospace" }}>
            Powered by FinBERT — a BERT model fine-tuned on financial text
          </p>
        </div>

        {/* Search */}
        <div style={{ display: "flex", gap: "0px", marginBottom: "36px", border: `2px solid ${colors.text}`, borderRadius: "2px", overflow: "hidden" }}>
          <input
            type="text"
            placeholder="Enter ticker symbol  —  AAPL, TSLA, NVDA..."
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            style={{
              flex: 1,
              background: colors.surface,
              border: "none",
              borderRight: `2px solid ${colors.text}`,
              padding: "14px 18px",
              color: colors.text,
              fontSize: "15px",
              outline: "none",
              fontFamily: "'Courier New', monospace",
              letterSpacing: "0.05em",
            }}
          />
          <button
            onClick={handleSearch}
            disabled={loading}
            style={{
              background: colors.text,
              border: "none",
              padding: "14px 32px",
              color: colors.bg,
              fontSize: "13px",
              fontWeight: "600",
              cursor: loading ? "not-allowed" : "pointer",
              fontFamily: "'Courier New', monospace",
              opacity: loading ? 0.6 : 1,
              letterSpacing: "0.1em",
              textTransform: "uppercase",
            }}
          >
            {loading ? "Analyzing..." : "Run Analysis"}
          </button>
        </div>

        {error && (
          <div style={{
            background: "transparent",
            border: `2px solid ${colors.negative}`,
            color: colors.negative,
            padding: "13px 18px",
            borderRadius: "2px",
            marginBottom: "24px",
            fontSize: "13px",
            fontFamily: "'Courier New', monospace",
          }}>
            ⚠ {error}
          </div>
        )}

        {avgSentiment !== null && (
          <>
            {/* Stat Cards */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "0px", marginBottom: "24px", border: `2px solid ${colors.border}` }}>
              {[
                { label: "Ticker", value: ticker, color: colors.text },
                { label: "Avg Sentiment Score", value: `${avgSentiment > 0 ? "+" : ""}${avgSentiment}`, color: getSentimentColor(sentimentLabel) },
                { label: "Sentiment", value: sentimentLabel, color: getSentimentColor(sentimentLabel) },
              ].map((item, i) => (
                <div key={i} style={{
                  padding: "24px",
                  borderRight: i < 2 ? `2px solid ${colors.border}` : "none",
                  background: colors.surface,
                }}>
                  <p style={{ color: colors.muted, fontSize: "10px", fontWeight: "600", textTransform: "uppercase", letterSpacing: "0.15em", margin: "0 0 10px 0", fontFamily: "'Courier New', monospace" }}>{item.label}</p>
                  <p style={{ fontSize: "32px", fontWeight: "700", margin: 0, color: item.color, fontFamily: "Georgia, serif", letterSpacing: "-0.5px" }}>{item.value}</p>
                </div>
              ))}
            </div>

            {/* Chart */}
            <div style={{ ...card, marginBottom: "24px" }}>
              <h2 style={{ fontSize: "10px", fontWeight: "600", margin: "0 0 24px 0", color: colors.muted, textTransform: "uppercase", letterSpacing: "0.15em", fontFamily: "'Courier New', monospace" }}>
                Price & Sentiment — Last 30 Days
              </h2>
              <ResponsiveContainer width="100%" height={280}>
                <ComposedChart data={chartData}>
                  <CartesianGrid strokeDasharray="2 4" stroke={colors.border} />
                  <XAxis dataKey="date" stroke={colors.border} tick={{ fontSize: 11, fill: colors.muted, fontFamily: "Courier New" }} />
                  <YAxis yAxisId="price" stroke={colors.border} tick={{ fontSize: 11, fill: colors.muted, fontFamily: "Courier New" }} domain={["auto", "auto"]} />
                  <YAxis yAxisId="sentiment" orientation="right" stroke={colors.border} tick={{ fontSize: 11, fill: colors.muted, fontFamily: "Courier New" }} domain={[-1, 1]} />
                  <Tooltip contentStyle={{
                    background: colors.surface,
                    border: `2px solid ${colors.border}`,
                    borderRadius: "2px",
                    fontSize: "12px",
                    color: colors.text,
                    fontFamily: "Courier New",
                  }} />
                  <Legend wrapperStyle={{ fontSize: "11px", color: colors.muted, fontFamily: "Courier New" }} />
                  <Line yAxisId="price" type="monotone" dataKey="price" stroke={colors.price} strokeWidth={2} dot={false} name="Price ($)" />
                  <Line yAxisId="sentiment" type="monotone" dataKey="sentiment" stroke={colors.sentiment} strokeWidth={2} dot={{ r: 4, fill: colors.sentiment }} name="Sentiment Score" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            {/* News Table */}
            <div style={card}>
              <h2 style={{ fontSize: "10px", fontWeight: "600", margin: "0 0 20px 0", color: colors.muted, textTransform: "uppercase", letterSpacing: "0.15em", fontFamily: "'Courier New', monospace" }}>
                News Feed — {articles.length} Articles Analyzed
              </h2>
              <div style={{ overflowY: "auto", maxHeight: "420px" }}>
                <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "13px" }}>
                  <thead>
                    <tr style={{ borderBottom: `2px solid ${colors.text}` }}>
                      {["Headline", "Source", "Date", "Sentiment"].map((h) => (
                        <th key={h} style={{ textAlign: "left", padding: "0 16px 12px 0", color: colors.muted, fontWeight: "600", fontSize: "10px", textTransform: "uppercase", letterSpacing: "0.15em", fontFamily: "'Courier New', monospace" }}>{h}</th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {articles.map((article, i) => (
                      <tr key={i} style={{ borderBottom: `1px solid ${colors.border}` }}>
                        <td style={{ padding: "14px 16px 14px 0", lineHeight: "1.5" }}>
                          <a href={article.url} target="_blank" rel="noreferrer" style={{ color: colors.text, textDecoration: "none", fontFamily: "Georgia, serif", fontSize: "14px" }}>
                            {article.title}
                          </a>
                        </td>
                        <td style={{ padding: "14px 16px", color: colors.muted, whiteSpace: "nowrap", fontFamily: "'Courier New', monospace", fontSize: "12px" }}>{article.source}</td>
                        <td style={{ padding: "14px 16px", color: colors.muted, whiteSpace: "nowrap", fontFamily: "'Courier New', monospace", fontSize: "12px" }}>{article.date}</td>
                        <td style={{ padding: "14px 0 14px 16px" }}>
                          <span style={getBadgeStyle(article.sentiment)}>
                            {article.sentiment} {article.score > 0 ? "+" : ""}{article.score}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}