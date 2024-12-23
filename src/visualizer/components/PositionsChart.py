import plotly.graph_objects as go

class PositionsChart:
    @staticmethod
    def show_chart(st, df):
        fig = go.Figure()
        fig.add_trace(
            go.Pie(
                labels=list(df["symbol"]),
                values=list(df["market_value"].abs()),
                sort=False
            )
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)