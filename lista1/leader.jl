using Base.Iterators
using PyPlot
using ArgParse

@enum Status NULL SINGLE COLLISION

mutable struct Generator
    xs::Vector{Any}
    idx::Int
end

function next!(gen::Generator)
    val = gen.xs[gen.idx]
    if gen.idx == length(gen.xs)
        gen.idx = 1
    else
        gen.idx += 1
    end
    val
end

function make_exact_generator(n_nodes::Int)
    Generator([1/n_nodes], 1)
end

function make_upper_bound_generator(upper_bound::Int)
    round_len = ceil(log2(upper_bound))
    round = [0.5^i for i in 1:round_len]
    Generator(round, 1)
end

function leader_election!(p_vector, n_nodes::Int)
    slot = NULL
    i = 0

    while slot != SINGLE
        i += 1
        slot = NULL
        prob = next!(p_vector)
        
        for node in 1:n_nodes
            if rand() <= prob    
                if slot === NULL
                    slot = SINGLE
                else
                    slot = COLLISION
                    break
                end
            end
        end
    end
    i
end

function zad1(n_tries::Int, n_nodes::Int)
    results = Vector{Int}()
    for i in 1:n_tries
        generator = make_exact_generator(n_nodes)
        result = leader_election!(generator, n_nodes)
        push!(results, result)
    end
    [(u, count(x->x==u, results)) for u in unique(results)]
end

function zad1(n_tries::Int, n_nodes::Int, upper_bound::Int)
    results = Vector{Int}()
    for i in 1:n_tries
        generator = make_upper_bound_generator(upper_bound)
        result = leader_election!(generator, n_nodes)
        push!(results, result)
    end
    [(u, count(x->x==u, results)) for u in unique(results)]
end

function zad2(n_tries::Int, n_nodes::Int, upper_bound::Int, is_upper_bound::Bool)
    if is_upper_bound
        results = zad1(n_tries, n_nodes, upper_bound)
    else
        results = zad1(n_tries, n_nodes)
    end

    plt = figure("Zadanie 2", figsize=(8,8))
    max_val = max([t[1] for t in results]...)
    bins = [i for i in 1:max_val+1]
    hist([t[1] for t in results], bins=bins, weights=[t[2] for t in results], histtype="bar", rwidth=0.5, align="left")
    grid()
    show()
end

function zad3(n_tries::Int, n_nodes::Int)
    results = zad1(n_tries, n_nodes)

    expected_val = sum([t[1] * t[2]/n_tries for t in results])

    avg = sum([t[1] * t[2] for t in results]) / n_tries
    variance = sum([(t[1] - avg)^2 for t in results for i in 1:t[2]]) / n_tries
    
    return expected_val, variance
end

function parse_cmdline()
    s = ArgParseSettings()

    @add_arg_table! s begin
        "zad1"
            help = "Zadanie 1."
            action = :command
        "zad2"
            help = "Zadanie 2"
            action = :command
        "zad3"
            help = "Zadanie 2"
            action = :command
        "zad4"
            help = "Zadanie 2"
            action = :command
    end

    for cmd in ["zad1", "zad2", "zad3", "zad4"]
        @add_arg_table! s[cmd] begin
            "-n", "--n_tries"
                help = "Ilość symulacji."
                arg_type = Int
                default = 1000
            "--u"
                help = "Scenariusz z ograniczeniem górnym."
                action = :store_true
            "n_nodes"
                help = "Liczba węzłów."
                required = true
                arg_type = Int
            "upper_bound"
                help = "Ograniczenie górne. (dla wartości -1 ograniczenie górne jest równe liczbie węzłów)"
                default = -1
                arg_type = Int
        end
    end
    
    return parse_args(s)
end

function print_config(n_tries, n_nodes, upper_bound, is_upper_bound)
    println("Liczba prób: $n_tries")
    println("Liczba węzłów: $n_nodes")
    if is_upper_bound
        println("Ograniczenie górne: $upper_bound")
    end
    println()
    nothing
end

function main()
    arguments = parse_cmdline()

    cmd = arguments["%COMMAND%"]

    n_nodes = arguments[cmd]["n_nodes"]
    upper_bound = arguments[cmd]["upper_bound"]
    is_upper_bound = arguments[cmd]["u"]
    n_tries = arguments[cmd]["n_tries"]
    
    if is_upper_bound && upper_bound < n_nodes
        upper_bound = n_nodes
    end

    print_config(n_tries, n_nodes, upper_bound, is_upper_bound)

    if cmd == "zad1"
        if is_upper_bound
            println("Zadanie 1, scenariusz 3")
            res = zad1(n_tries, n_nodes, upper_bound)
        else
            println("Zadanie 1, scenariusz 2")
            res = zad1(n_tries, n_nodes)
        end
        println("\nWynik:")
        for t in sort(res)
            print("($(t[1]), $(t[2])) ")
        end
        println()

    elseif cmd == "zad2"
        println("Zadanie 2")
        zad2(n_tries, n_nodes, upper_bound, is_upper_bound)
    
    elseif cmd == "zad3"
        println("Zadanie 3")
        expected_val, variance = zad3(n_tries, n_nodes)
        println("E[L] = $expected_val\nVar[L] = $variance")

    elseif cmd == "zad4"

    else

    end
end

main()