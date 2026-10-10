from traffic_simulator import TrafficSimulator
from rich.console import Console
from rich.table import Table

console = Console()

def run_resiliency_test():
    console.print("\n[bold cyan]🛡️  API Rate Guard - Resiliency Verification Suite[/bold cyan]\n")
    console.print("[yellow]Simulating burst traffic: 10 requests sent rapidly (0.1s interval)...[/yellow]\n")
    
    simulator = TrafficSimulator()
    results = simulator.send_burst_traffic(total_requests=10, delay_between_requests=0.1)
    
    # Create Rich Console Table
    table = Table(title="Rate Limiter Execution Telemetry")
    table.add_column("Seq #", justify="center", style="cyan")
    table.add_column("Timestamp", justify="center")
    table.add_column("Status Code", justify="center")
    table.add_column("Tokens Left", justify="center", style="magenta")
    table.add_column("Audit Outcome", justify="left")

    for row in results:
        status_style = "green" if row["status_code"] == 200 else "red"
        table.add_row(
            str(row["request_seq"]),
            row["time"],
            f"[{status_style}]{row['status_code']}[/{status_style}]",
            row["remaining_tokens"],
            f"[{status_style}]{row['outcome']}[/{status_style}]"
        )

    console.print(table)
    console.print("\n[bold green]✅ Telemetry collection completed successfully.[/bold green]\n")

if __name__ == "__main__":
    run_resiliency_test()