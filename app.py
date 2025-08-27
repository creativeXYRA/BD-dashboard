import os
import dash
from dash import html, dcc
import logging
import pandas as pd
import plotly.express as px

# 設定日誌，方便除錯和查看 Cloud Run 的日誌
logging.basicConfig(level=logging.INFO)
logging.info("啟動 Dash 應用程式...")

# 從環境變數中取得 Cloud Run 指定的埠號。
# 如果本地運行，預設為 8080。
port = int(os.environ.get('PORT', 8080))
logging.info(f"使用的埠號: {port}")

# 建立 Dash 應用程式實例
# 我們需要使用 `server = app.server`，這是 gunicorn 所需要的。
app = dash.Dash(__name__)
server = app.server

# --------------------------------------------------------------------------------
# 在這裡加入你的資料處理和函式
# --------------------------------------------------------------------------------
# 範例：建立一個簡單的 DataFrame
data = {
    '類別': ['A', 'B', 'C', 'D', 'E'],
    '值': [10, 25, 15, 30, 20]
}
df = pd.DataFrame(data)

# 範例：使用 Plotly 建立長條圖
fig = px.bar(df, x='類別', y='值', title='範例長條圖')

# --------------------------------------------------------------------------------
# 定義 Dash 應用程式的佈局 (Layout)
# --------------------------------------------------------------------------------
app.layout = html.Div(
    className="container mx-auto p-4 bg-gray-100 min-h-screen",
    children=[
        html.H1("我的 Dash 儀表板", className="text-4xl font-bold text-center text-blue-800 mb-6"),
        
        # 範例段落
        html.P(
            "這是一個部署到 Cloud Run 的範例 Dash 應用程式。",
            className="text-lg text-gray-700 text-center mb-8"
        ),

        # 包含圖表的容器
        html.Div(
            className="bg-white p-6 rounded-lg shadow-md",
            children=[
                dcc.Graph(
                    id='my-graph',
                    figure=fig
                )
            ]
        ),
        
        # 腳註
        html.P(
            "由你提供的程式碼生成，可以自由修改和擴展。",
            className="text-sm text-gray-500 text-center mt-12"
        )
    ]
)

# --------------------------------------------------------------------------------
# 執行應用程式
# --------------------------------------------------------------------------------
# 這個區塊確保應用程式在本地或 Cloud Run 上都能正確運行
if __name__ == '__main__':
    logging.info("在本地環境運行伺服器...")
    app.run_server(host='0.0.0.0', port=port, debug=False)
