import click
from math import ceil, log2
from matplotlib import pyplot as plt
from leader_election import leader_election, leader_election_n_times, plot_hist, calc_expected_value, calc_variance, Scenario

scenarios_dict = {
    'second': Scenario.SECOND,
    'third': Scenario.THIRD
}

@click.group()
@click.option('--scenario', '-s', 'scenario', default='second', required=False, type=click.Choice(['second', 'third'], case_sensitive=False))
@click.option('--n-times', '-n', 'n', default=10000, required=False, type=int)
@click.pass_context
def cli(ctx, scenario, n):
    ctx.ensure_object(dict)

    assert(n > 0)
    ctx.obj['SCENARIO'] = scenario
    ctx.obj['N_TIMES'] = n

@cli.command('zad1', help='Lista 1 zadanie 1')
@click.argument('n_nodes', type=int, required=True)
@click.argument('upper_bound', type=int, required=False, default=-1)
@click.pass_context
def run1(ctx, n_nodes, upper_bound):
    """
    Zadanie 1
    """
    assert(n_nodes > 1)
    n_times = ctx.obj['N_TIMES']
    scenario = scenarios_dict[ctx.obj['SCENARIO']]

    results = {}
    for i in range(0, n_times):
        result = leader_election(n_nodes, upper_bound, scenario)
        m = results.get(result, 0)
        m += 1
        results[result] = m
    
    res_list = []
    for k, v in results.items():
        res_list.append((k, v))
    res_list.sort()
    click.echo(res_list)


@cli.command('zad2', help='Lista 1 zadanie 2')
@click.argument('n_nodes', type=int, required=True)
@click.argument('upper_bound', type=int, required=False, default=-1)
@click.pass_context
def run2(ctx, n_nodes, upper_bound):
    """
    Zadanie 2
    """
    assert(n_nodes > 1)
    n_times = ctx.obj['N_TIMES']
    scenario = scenarios_dict[ctx.obj['SCENARIO']]

    res_list = leader_election_n_times(n_nodes, upper_bound, scenario, n_times)
    plot_hist(res_list)

@cli.command('zad3', help='Lista 1 zadanie 3')
@click.argument('n_nodes', type=int, required=True)
@click.pass_context
def run3(ctx, n_nodes):
    """
    Zadanie 3
    """
    assert(n_nodes > 1)
    n_times = ctx.obj['N_TIMES']
    
    res_list = leader_election_n_times(n_nodes, n_nodes, Scenario.SECOND, n_times)
    expected_val = calc_expected_value(res_list)
    variance = calc_variance(res_list)
    click.echo('Expected value: {}\nVariance: {}'.format(expected_val, variance))

@cli.command('zad4', help='Lista 1 zadanie 4')
@click.argument('upper_bound', type=int, required=False, default=None)
@click.pass_context
def run4(ctx, upper_bound):
    """
    Zadanie 4
    """
    assert(upper_bound > 1)
    n_times = ctx.obj['N_TIMES']
    lam = 0.579 # lambda value
    errors = []

    round_len = ceil(log2(upper_bound)) # length of single round
    prob_list = [] # for plotting

    for n_nodes in range(upper_bound, 1, -1):
        res_list = leader_election_n_times(n_nodes, upper_bound, Scenario.THIRD, n_times)
        res_list = res_list[0:round_len]
        # Pr[S_{L,n}]
        pr = sum([v for k,v in res_list])/n_times
        if pr < lam:
            errors.append((n_nodes, pr))

        if n_nodes % 5 == 0:
            prob_list.append((n_nodes, pr))

    if errors:
        click.echo('Fail.')
        for k,v in errors:
            click.echo(f'Nodes: {k}  Pr: {v}')
    else:
        click.echo('Success.')

    prob_list.sort()
    # bins - intervals for histogram (value of n in each experiment)
    bins = [k for k,v in prob_list]
    bins.append(bins[-1]+5)
    
    plt.figure(figsize=(8,8))
    plt.hist([k for k,v in prob_list],
             bins=bins,
             weights=[v for k,v in prob_list],
             align='left',
             rwidth=0.2)
    plt.xlabel('Liczba węzłów')
    plt.ylabel('Szacowane P[S_(L,n)]')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    cli(obj={})
