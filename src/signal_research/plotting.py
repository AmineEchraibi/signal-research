import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def plot_price_and_indicators(df, symbol:str, indicators:list[str], x_axis="date"):
    fig = go.Figure()
    colors = px.colors.qualitative.Plotly
    
    for i, indicator in enumerate(indicators):
        name = indicator[0]
        type_ = indicator[1]
        color = colors[i % len(colors)]
        if type_ == "lines":
            fig.add_trace(go.Scatter(
                x=df[x_axis],
                y=df[name],
                mode=type_,
                name=name,
                line=dict(color=color)
            ))
        elif type_ == "confidence":
            fig.add_trace(go.Scatter(x=df[x_axis], y=df[f"{name}_upper"], mode='lines', name=f"{name}_upper", line=dict(color=color)))
            fig.add_trace(go.Scatter(x=df[x_axis], y=df[f"{name}_lower"], mode='lines', name=f"{name}_lower", line=dict(color=color)))

        elif type_ == "chart":
            fig.add_trace(
                go.Candlestick(
                    x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='Price'
                ),
            )
        else:
            raise Exception(f"Type not implemented {type_}")
                    
    
    # Update layout with titles and labels
    fig.update_layout(
        title=f'symbol == {symbol}',
        xaxis_title='Date',
        yaxis_title='Price',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly",
    )

    # Display the figure
    fig.show()



def plot_histogram(df, column, buy_only=True):
    if buy_only:
        df = df[df['signal'] == 1]
    fig = px.histogram(df, 
                    x=column, 
                    nbins=100,  # Adjust the number of bins as needed
                    title=f'{column} Distribution',
                    marginal='box',  # Optionally adds a box plot on the histogram for more insight
                    opacity=0.75)  # Set transparenc
    # Customize layout
    fig.update_layout(
        xaxis_title=column,
        yaxis_title='Frequency',
        bargap=0.1  # Adjust the gap between bars
    )

    fig.show()
    
    
def plot_buy_sell_signals(df, buy_only=True):
    buy_signals = df[df['signal'] == 1]
    
    

    fig = go.Figure()
    fig.add_trace(
                go.Candlestick(
                    x=df['date'],
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'],
                    name='Price'
                ),
            )

    fig.add_trace(go.Scatter(
        x=buy_signals['date'], y=buy_signals['close'],
        mode='markers', marker=dict(size=15, color='green', symbol='circle'),
        name='Buy Signal'
    ))

    # Add Sell signals with big red markers
    if not buy_only:
        sell_signals = df[df['signal'] == -1]
        fig.add_trace(go.Scatter(
            x=sell_signals['date'], y=sell_signals['close'],
            mode='markers', marker=dict(size=15, color='red', symbol='circle'),
            name='Sell Signal'
        ))

    # Update layout for better visualization
    fig.update_layout(
        title="Buy and Sell Signals",
        xaxis_title="Date",
        yaxis_title="Close Price",
        legend_title="Signals",
        height=600
    )
    fig.show()
