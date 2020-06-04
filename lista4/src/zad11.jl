using Plots


function nakamoto(n, q)
    p = 1.0 - q
    l = n * (q / p)
    s = 1.0
    for i = 0:n
        possion = exp(-l)
        for j = 1:i
            possion *= l / j
        end
        s -= possion * (1 - (q/p)^(n-i))
    end
    return s
end

function nakamoto_limit(limit, q, start_n=0)
    n = start_n
    result = 1.0
    while result > limit
        n += 1
        result = nakamoto(n, q)
    end
    return n
end


function grunspan(n, q)
    p = 1-q
    s = 1.0
    for k = 0:n-1
        s -= (p^n * q^k - q^n * p^k) * binomial(big(k+n-1), big(k))
    end
    return s
end

function grunspan_limit(limit, q, start_n=0)
    n = start_n
    result = 1.0
    while result > limit
        n += 1
        result = grunspan(n, q)
    end
    return n
end


function plot1(n)
    nakamoto_results = Vector{Float64}()
    grunspan_results = Vector{Float64}()
    q_range = 0.001:0.001:0.49
    for q in q_range
        append!(nakamoto_results, nakamoto(n, q))
        append!(grunspan_results, grunspan(n, q))
    end

    p = plot(q_range, [nakamoto_results, grunspan_results], label=["Nakamoto" "Grunspan"], xlabel="q", ylabel="P(n,q)", title="n = $n", legend=:top, linewidth=2)
    savefig(p, "n=$n.png")
end


function plot2(limit)
    nakamoto_results = Vector{Int64}()
    grunspan_results = Vector{Int64}()
    q_range = 0.001:0.001:0.44

    for q in q_range
        append!(nakamoto_results, nakamoto_limit(limit, q))
        append!(grunspan_results, grunspan_limit(limit, q))
    end

    p = plot(q_range, [nakamoto_results, grunspan_results], label=["Nakamoto" "Grunspan"], xlabel="q", ylabel="n", title="P(n,q) <= $(limit*100)%", legend=:top, linewidth=2)
    savefig(p, "limit=$limit.png")
end


function simulation(n, q)
    adv_blocks = 0
    usr_blocks = 0
    p = 1.0 - q

    while usr_blocks < n
        r = rand()
        if r < q
            adv_blocks += 1
        else
            usr_blocks += 1
        end
    end
    if adv_blocks >= usr_blocks
        return 1.0
    else
        return (q/p)^(usr_blocks - adv_blocks)
    end
end

function monte_carlo_simulation(n, q, times)
    results = Vector{Float64}()
    for i = 1:times
        append!(results, simulation(n, q))
    end
    return reduce(+, results) / times
end


function plot_m_c(n)
    nakamoto_results = Vector{Float64}()
    grunspan_results = Vector{Float64}()
    monte_carlo_results = Vector{Float64}()
    q_range = 0.005:0.005:0.49

    for q in q_range
        append!(nakamoto_results, nakamoto(n, q))
        append!(grunspan_results, grunspan(n, q))
        append!(monte_carlo_results, monte_carlo_simulation(n, q, 100000))
    end

    p = plot(q_range, [nakamoto_results, grunspan_results], label=["Nakamoto" "Grunspan"], xlabel="q", ylabel="P(n,q)", title="n = $n", linewidth=2)
    scatter!(q_range, monte_carlo_results, label="MonteCarlo", legend=:top, markersize=3)
    savefig(p, "mc_n=$n.png")
end


function plot_m_c_to_grunspan(n)
    results = Vector{Float64}()
    q_range = 0.01:0.005:0.49

    for q in q_range
        g = grunspan(n, q)
        mc = monte_carlo_simulation(n, q, 100000)
        append!(results, mc/g)
    end

    p = scatter(q_range, results, label="sim/gru ratio", markersize=3, xlabel="q", ylabel="Ratio", title="Simulation to Grunspan ratio for n = $n")
end


function plot_m_c_to_nakamoto(n)
    results = Vector{Float64}()
    q_range = 0.01:0.005:0.49

    for q in q_range
        na = nakamoto(n, q)
        mc = monte_carlo_simulation(n, q, 100000)
        append!(results, mc/na)
    end

    p = scatter(q_range, results, label="sim/nak ratio", markersize=3, xlabel="q", ylabel="Ratio", title="Simulation to Nakamoto ratio for n = $n")
end


for n in [1, 3, 6, 12, 24, 48]
    plot1(n)
    plot_m_c(n)
    plot_m_c_to_grunspan(n)
    plot_m_c_to_nakamoto(n)
end

for limit in [0.1, 0.01, 0.001]
    plot2(limit)
end
