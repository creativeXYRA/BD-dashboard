# Asymchem BD Dashboard Complete Code with English-only Display and Hover Tooltips

# Step 1: Environment Setup
# Note: For Google Colab, you need to install the cytoscape library.
!pip install dash-cytoscape

# Step 2: Imports
from dash import Dash, html, dcc, dash_table, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import json
import re
import dash_cytoscape as cyto

# Step 3: Prepare Data
# Market Data for Bubble Chart
market_data = [
    {'company': 'CRISPR Therapeutics', 'business_potential': 500, 'tech_mapping': 8, 'market_value': 1000, 'pain_point': 'Scalability', 'focus': 'Gene therapy and CRISPR-based treatments', 'solution': 'Asymchem’s biocatalysis reduces impurities by 20% for vector purification.'},
    {'company': 'Mersana Therapeutics', 'business_potential': 300, 'tech_mapping': 6, 'market_value': 600, 'pain_point': 'Cost', 'focus': 'ADC development for oncology', 'solution': 'Asymchem’s OEB5 facility cuts solvent waste by 25%.'},
    {'company': 'LaNova Medicines', 'business_potential': 200, 'tech_mapping': 7, 'market_value': 400, 'pain_point': 'Regulatory', 'focus': 'ADC and biologics in APAC markets', 'solution': 'Asymchem’s STAR AI optimizes yields 15% faster.'},
    {'company': 'Beam Therapeutics', 'business_potential': 350, 'tech_mapping': 7.5, 'market_value': 700, 'pain_point': 'Efficiency', 'focus': 'Base editing therapies', 'solution': 'Asymchem’s flow chemistry improves efficiency.'},
    {'company': 'Sana Biotechnology', 'business_potential': 250, 'tech_mapping': 6.5, 'market_value': 500, 'pain_point': 'Yield', 'focus': 'Cell and gene therapy platforms', 'solution': 'Asymchem’s biocatalysis boosts yield for cell therapy vectors.'},
    {'company': 'Intellia Therapeutics', 'business_potential': 400, 'tech_mapping': 8.5, 'market_value': 800, 'pain_point': 'Scalability', 'focus': 'CRISPR/Cas9 therapeutics', 'solution': 'Asymchem’s OEB5 facility supports multi-kg scaling.'},
    {'company': 'Moderna', 'business_potential': 450, 'tech_mapping': 9, 'market_value': 900, 'pain_point': 'Cost', 'focus': 'mRNA-based therapies', 'solution': 'Asymchem’s STAR AI optimizes mRNA production costs.'},
    {'company': 'Verve Therapeutics', 'business_potential': 280, 'tech_mapping': 6.8, 'market_value': 560, 'pain_point': 'Regulatory', 'focus': 'Gene editing for cardiovascular diseases', 'solution': 'Asymchem’s biocatalysis ensures regulatory compliance.'},
    {'company': 'Caribou Biosciences', 'business_potential': 320, 'tech_mapping': 7.2, 'market_value': 640, 'pain_point': 'Yield', 'focus': 'CRISPR genome engineering', 'solution': 'Asymchem’s flow chemistry enhances yield.'},
    {'company': 'Editas Medicine', 'business_potential': 270, 'tech_mapping': 6.3, 'market_value': 540, 'pain_point': 'Efficiency', 'focus': 'Gene editing for inherited diseases', 'solution': 'Asymchem’s OEB5 facility improves efficiency.'}
]

# BD Data for Table and Network (now with updated connections)
bd_data = [
    {
        'name': 'Adam Macnaughton',
        'company': 'CRISPR Therapeutics',
        'email': 'adam.macnaughton@crisprtx.com',
        'linkedin': 'https://www.linkedin.com/in/adam-macnaughton-502482149',
        'school': 'Harvard Business School',
        'connections': 'Cheng Yi Chen: Shared Merck and Bristol Myers Squibb network; Becky: Attended BIO 2025; James Gage: Harvard University alumni network',
        'action': 'Email Sep 10, 2025: Pitch biocatalysis for vector purification'
    },
    {
        'name': 'Sam Kay',
        'company': 'Mersana Therapeutics',
        'email': 'sam.kay@mersana.com',
        'linkedin': 'https://www.linkedin.com/in/swkay',
        'school': 'McGill University',
        'connections': 'Becky: Attended BIO 2025; Cheng Yi Chen: Merck network via Immunomedics/Gilead deal; You: Novartis network; Xinhui Hu: Roche R&D background',
        'action': 'Becky meets at CPHI, pitch OEB5 for ADC linker scaling'
    },
    {
        'name': 'Paul Kong',
        'company': 'LaNova Medicines',
        'email': 'paul.kong@lanovamed.com',
        'linkedin': 'https://www.linkedin.com/in/paul-kong-lanova',
        'school': 'Shanghai Jiao Tong University School of Medicine',
        'connections': 'Xinhui Hu: Shared Roche and Everest Medicines experience; Cheng Yi Chen: Merck network via LaNova deal; Elut Hsu: Shared background in China',
        'action': 'Email Sep 5, 2025: Pitch OEB5 for ADC scaling'
    }
]

# Asymchem Leadership Team Data for Network
# Note: This data is used to enrich the network graph with key internal personnel.
leadership_data = [
    {'name': 'Hao Hong', 'title': 'Chairman & Co-CEO', 'key_connections': 'West China Medical Center; Capital Medical University; Chinese Academy of Medical Sciences'},
    {'name': 'James Gage', 'title': 'CSO', 'key_connections': 'Pfizer; Harvard University (Ph.D.)'},
    {'name': 'Xinhui Hu', 'title': 'CTO', 'key_connections': 'GlaxoSmithKline; Roche; Everest Medicines; Brown University'},
    {'name': 'Cheng Yi Chen', 'title': 'CTO', 'key_connections': 'Bristol Myers Squibb; Mirati; Janssen; Merck; The Ohio State University; Xiamen University'},
    {'name': 'Rui Yang', 'title': 'Co-CEO', 'key_connections': 'Peking University; Tianjin University'},
    {'name': 'Xin Xin Zhi', 'title': 'Chairman-Supervisory Board', 'key_connections': 'Missouri State University'},
    {'name': 'Elut Hsu', 'title': 'President & GM', 'key_connections': 'University of Hong Kong; North Carolina State University'},
    {'name': 'Da Zhang', 'title': 'Director, COO & CFO', 'key_connections': 'Tsinghua University; Tianjin University'}
]
bd_team_data = [
    {'name': 'Becky', 'title': 'Sr. Director of BD', 'key_connections': 'Catalent; Primera Analytical Solutions; BIO 2025; CPHI'},
    {'name': 'You', 'title': 'BD Director', 'key_connections': 'Novartis; Merck; shared network'}
]

df_market = pd.DataFrame(market_data)
df_bd = pd.DataFrame(bd_data)

# Step 4: Dashboard Layout with Market Analysis Table
app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'])

# Define figures outside of the layout for proper initialization
fig_bubble = go.Figure(data=[
    go.Scatter(
        x=df_market['business_potential'],
        y=df_market['tech_mapping'],
        mode='markers',
        marker=dict(
            # Bubble size is now scaled more effectively
            size=df_market['market_value'] / 5,
            sizemode='area',
            sizemin=10,
            color=df_market['tech_mapping'],
            colorscale='Viridis',
            showscale=True
        ),
        text=df_market['company'] + '<br>Pain Point: ' + df_market['pain_point'] + '<br>Potential: $' + df_market['business_potential'].astype(str) + 'M' + '<br>Focus: ' + df_market['focus'] + '<br>Solution: ' + df_market['solution'],
        hoverinfo='text'
    )
])
fig_bubble.update_layout(
    title='Market Prioritization: Biosynthesis Opportunities',
    xaxis_title='Business Potential ($M)',
    yaxis_title='Tech Mapping (0-10)',
    plot_bgcolor='#111827',
    paper_bgcolor='#111827',
    font=dict(color='white')
)

# New function to create a more sophisticated network graph with hover tooltips
def create_network_elements(df_bd, leadership_data, bd_team_data):
    """
    Creates elements (nodes and edges) for a dash-cytoscape graph, with node size
    based on connection count. Nodes are only people. Connections are in tooltips.
    """
    all_people_list = leadership_data + bd_team_data + df_bd.to_dict('records')
    node_connections_count = {}
    
    # Map person's name to their data for easy lookup
    person_data_map = {p['name']: p for p in all_people_list}
    
    # First pass: Count connections for people only. Connections are other people.
    for person in all_people_list:
        conn_str = person.get('key_connections') or person.get('connections')
        if conn_str:
            connections = re.split(';|,', conn_str) # Split by semicolon or comma
            for conn in connections:
                # Find other people names in the connection string
                for other_person in all_people_list:
                    if other_person['name'] in conn:
                        # Increment connection count for both parties
                        node_connections_count[person['name']] = node_connections_count.get(person['name'], 0) + 1
                        node_connections_count[other_person['name']] = node_connections_count.get(other_person['name'], 0) + 1
    
    # Create person nodes with sizes based on connection count
    nodes = []
    max_connections = max(node_connections_count.values()) if node_connections_count else 1
    
    for person in all_people_list:
        conn_count = node_connections_count.get(person['name'], 0)
        # Scale size from 20 to 80
        node_size = 20 + (conn_count / max_connections) * 60 
        
        # Determine the person's role/type for styling
        node_class = 'bd_person' if person.get('company') and person['company'] != 'Asymchem' else 'leader'
        
        # Prepare hover tooltip content
        title = person.get('title', 'BD Director' if 'You' in person['name'] else 'Client')
        company = person.get('company', 'Asymchem')
        
        # Format connections into a readable list
        connections_str = person.get('connections') or person.get('key_connections')
        connection_details = ""
        if connections_str:
            connections = re.split(';|,', connections_str)
            connection_details = "<br><b>Connections:</b>"
            for conn in connections:
                clean_conn = conn.strip()
                # Use regex to find the person's name and the specific connection detail
                match = re.match(r'(.*?):(.*)', clean_conn)
                if match:
                    person_name, detail = match.groups()
                    connection_details += f"<br>- {person_name.strip()}: {detail.strip()}"
                else:
                    connection_details += f"<br>- {clean_conn}"

        tooltip = f"""
        <b>{person['name']}</b>
        <br>Title: {title}
        <br>Company: {company}
        {connection_details}
        """

        nodes.append({
            'data': {
                'id': person['name'],
                'label': person['name'],
                'size': node_size,
                'tooltip': tooltip
            },
            'classes': node_class
        })
    
    # Create edges between people who are connected
    edges = []
    processed_edges = set() # Prevent duplicate edges
    for person in all_people_list:
        conn_str = person.get('key_connections') or person.get('connections')
        if conn_str:
            connections = re.split(';|,', conn_str)
            for conn in connections:
                clean_conn = conn.strip()
                for other_person in all_people_list:
                    if other_person['name'] in clean_conn and person['name'] != other_person['name']:
                        edge_id = tuple(sorted((person['name'], other_person['name'])))
                        if edge_id not in processed_edges:
                            edges.append({'data': {'source': person['name'], 'target': other_person['name']}})
                            processed_edges.add(edge_id)
                            
    return nodes + edges


# Initialize the app and layout with Tailwind CSS
app.layout = html.Div(
    className="bg-gray-900 text-white min-h-screen p-8 font-sans",
    children=[
        # Stores the BD data as a JSON string
        dcc.Store(id='bd-data-store', data=df_bd.to_json(date_format='iso', orient='split')),

        html.H1("Asymchem BD Dashboard", className="text-4xl font-bold text-center mb-8 text-indigo-400"),

        # Market Prioritization Section
        html.Div(
            className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8",
            children=[
                html.H2("Market Prioritization", className="text-2xl font-semibold mb-4 text-indigo-300 text-right"),
                dcc.Graph(id='bubble-chart', figure=fig_bubble, className="rounded-lg"),
            ]
        ),

        # Market Analysis Table Section
        html.Div(
            className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8",
            children=[
                html.H2("Market Analysis Table", className="text-2xl font-semibold mb-4 text-indigo-300 text-right"),
                dash_table.DataTable(
                    id='market-analysis-table',
                    columns=[
                        {'name': 'Company', 'id': 'company'},
                        {'name': 'Potential ($M)', 'id': 'business_potential'},
                        {'name': 'Tech Mapping (0-10)', 'id': 'tech_mapping'},
                        {'name': 'Market Value ($M)', 'id': 'market_value'},
                        {'name': 'Pain Point', 'id': 'pain_point'},
                        {'name': 'Focus', 'id': 'focus'},
                        {'name': 'Solution', 'id': 'solution'}
                    ],
                    data=df_market.to_dict('records'),
                    style_table={'overflowX': 'auto', 'textAlign': 'right'},
                    style_cell={
                        'backgroundColor': '#1f2937', # gray-800
                        'color': 'white',
                        'fontFamily': 'sans-serif',
                        'padding': '12px',
                        'border': '1px solid #374151', # gray-700
                        'textAlign': 'right'
                    },
                    style_header={
                        'backgroundColor': '#4338ca', # indigo-700
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textTransform': 'uppercase',
                        'padding': '12px',
                        'textAlign': 'right'
                    }
                ),
            ]
        ),

        # BD Personnel Network Section with dynamic inputs
        html.Div(
            className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8",
            children=[
                html.H2("BD Personnel Network", className="text-2xl font-semibold mb-4 text-indigo-300 text-right"),
                html.P("Enter the person's name and connections here to dynamically update the network graph.", className="text-gray-400 mb-4 text-right"),
                html.Div(
                    className="flex flex-col space-y-4 mb-4 items-end",
                    children=[
                        dcc.Input(id='new-name-input', type='text', placeholder='Enter Name...', className='bg-gray-700 p-3 rounded-md text-white border border-gray-600 w-full'),
                        dcc.Input(id='new-company-input', type='text', placeholder='Enter Company...', className='bg-gray-700 p-3 rounded-md text-white border border-gray-600 w-full'),
                        dcc.Textarea(id='new-connections-input', placeholder='Enter Connections... (e.g., Becky: CPHI 2025; Chen: Merck network)', className='bg-gray-700 p-3 rounded-md text-white border border-gray-600 w-full'),
                        html.Button('Add to Network', id='add-person-button', n_clicks=0, className="px-6 py-3 rounded-md font-bold text-gray-900 bg-indigo-400 hover:bg-indigo-300 transition-colors duration-200")
                    ]
                ),
                cyto.Cytoscape(
                    id='network-graph',
                    layout={'name': 'cose'},
                    style={'width': '100%', 'height': '500px', 'backgroundColor': '#1f2937', 'borderRadius': '0.5rem'},
                    stylesheet=[
                        {
                            'selector': 'node',
                            'style': {
                                'label': 'data(label)',
                                'text-valign': 'bottom',
                                'text-halign': 'center',
                                'font-family': 'sans-serif',
                                'font-size': '10px',
                                'color': 'white',
                                'height': 'data(size)',
                                'width': 'data(size)',
                                'border-width': 2,
                                'border-color': '#111827',
                                'text-wrap': 'wrap',
                                'text-max-width': '60px',
                                'background-color': '#60a5fa' # Blue for all people nodes
                            }
                        },
                        {
                            'selector': '.leader',
                            'style': {
                                'background-color': '#f59e0b', # Yellow for leaders
                            }
                        },
                        {
                            'selector': '.bd_person',
                            'style': {
                                'background-color': '#f87171', # Red for BD people
                            }
                        },
                        {
                            'selector': 'edge',
                            'style': {
                                'line-color': '#4b5563', # Gray
                                'width': 1,
                                'curve-style': 'bezier',
                            }
                        }
                    ],
                    elements=create_network_elements(df_bd, leadership_data, bd_team_data)
                ),
                html.P("Hover over nodes to see details. Node size indicates the number of connections.", className="text-gray-400 mb-4 text-right"),
                dash_table.DataTable(
                    id='bd-personnel-table',
                    columns=[{'name': i, 'id': i} for i in df_bd.columns],
                    data=df_bd.to_dict('records'),
                    style_table={'overflowX': 'auto', 'textAlign': 'right'},
                    style_cell={
                        'backgroundColor': '#1f2937',
                        'color': 'white',
                        'fontFamily': 'sans-serif',
                        'padding': '12px',
                        'border': '1px solid #374151',
                        'textAlign': 'right'
                    },
                    style_header={
                        'backgroundColor': '#4338ca',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'textTransform': 'uppercase',
                        'padding': '12px',
                        'textAlign': 'right'
                    }
                ),
            ]
        ),

        # Generate Pitch Section
        html.Div(
            className="bg-gray-800 p-6 rounded-lg shadow-lg mb-8",
            children=[
                html.H2("Confirm & Generate Pitch", className="text-2xl font-semibold mb-4 text-indigo-300 text-right"),
                html.Div(
                    className="flex items-center space-x-4 mb-4 justify-end",
                    children=[
                        dcc.Dropdown(
                            id='company-dropdown',
                            options=[{'label': d['company'], 'value': d['company']} for d in bd_data],
                            value='CRISPR Therapeutics',
                            className="bg-gray-700 text-white rounded-md flex-grow",
                            style={'width': '100%'}
                        ),
                        html.Button(
                            'Generate Pitch',
                            id='pitch-button',
                            n_clicks=0,
                            className="px-6 py-3 rounded-md font-bold text-gray-900 bg-indigo-400 hover:bg-indigo-300 transition-colors duration-200"
                        )
                    ]
                ),
                html.Div(
                    id='pitch-output',
                    className="bg-gray-700 p-4 rounded-lg text-white text-left"
                ),
            ]
        ),

        # Assumptions and Sources Section
        html.Div(
            className="bg-gray-800 p-6 rounded-lg shadow-lg text-right",
            children=[
                html.P('Assumptions: Data is based on public reports, events, and alumni networks for reference only.', className="text-sm text-gray-400 mb-2"),
                html.P('Data Sources:', className="text-sm font-semibold text-gray-400"),
                html.A('LinkedIn', href='https://www.linkedin.com', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Company Websites', href='https://www.crisprtx.com', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Public News', href='https://www.merck.com/news', target='_blank', className="text-blue-400 hover:underline text-sm mr-4"),
                html.A('Event Schedules', href='https://www.cphi.com', target='_blank', className="text-blue-400 hover:underline text-sm")
            ]
        )
    ]
)

# Callbacks
# Callback to add new person to the BD data and update the table and network graph
@app.callback(
    Output('bd-data-store', 'data'),
    Output('bd-personnel-table', 'data'),
    Output('network-graph', 'elements'),
    Input('add-person-button', 'n_clicks'),
    State('new-name-input', 'value'),
    State('new-company-input', 'value'),
    State('new-connections-input', 'value'),
    State('bd-data-store', 'data')
)
def update_bd_data(n_clicks, new_name, new_company, new_connections, current_data):
    if not n_clicks or not new_name or not new_company or not new_connections:
        # If no button click or missing data, do nothing
        raise dash.exceptions.PreventUpdate

    # Parse current data
    df_bd_current = pd.read_json(current_data, orient='split')

    # Create new person entry
    new_person = {
        'name': new_name,
        'company': new_company,
        'email': '',  # Not provided in the input, so leave it empty
        'linkedin': '',
        'school': '',
        'connections': new_connections,
        'action': ''
    }

    # Append new person and convert back to DataFrame
    df_bd_updated = pd.concat([df_bd_current, pd.DataFrame([new_person])], ignore_index=True)

    # Return updated data for the store, table, and network graph
    updated_data_dict = df_bd_updated.to_dict('records')
    updated_elements = create_network_elements(df_bd_updated, leadership_data, bd_team_data)

    return df_bd_updated.to_json(date_format='iso', orient='split'), updated_data_dict, updated_elements

# Callback to generate the pitch based on the dropdown selection
@app.callback(
    Output('pitch-output', 'children'),
    Input('pitch-button', 'n_clicks'),
    State('company-dropdown', 'value'),
    State('bd-data-store', 'data')
)
def generate_pitch(n_clicks, company_name, current_data):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    
    # Reload the data from the store
    df_bd_current = pd.read_json(current_data, orient='split')

    # Find the matching BD data
    target_bd = df_bd_current[df_bd_current['company'] == company_name]
    if target_bd.empty:
        return "No BD data found for this company."

    target_bd_row = target_bd.iloc[0]

    # Find the corresponding market data
    target_market = df_market[df_market['company'] == company_name]
    if target_market.empty:
        return "No market data found for this company."

    target_market_row = target_market.iloc[0]
    
    pitch_text = f"""
    Pitch for {target_bd_row['name']} at {target_bd_row['company']}:

    Hi {target_bd_row['name']},

    I noticed that {target_bd_row['company']}'s key focus is {target_market_row['focus']}.
    Asymchem’s solution addresses your pain point of {target_market_row['pain_point']} with our {target_market_row['solution']}.

    We have a shared connection via {target_bd_row['connections']}. I would like to connect to discuss how we can help you scale your {target_market_row['focus']} pipeline.
    """
    return dcc.Markdown(pitch_text)

# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True)
