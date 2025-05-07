import subprocess

def run_gap_code(gap_code):
    process = subprocess.Popen(['gap', '-q'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, error = process.communicate(gap_code)
    if process.returncode != 0:
        raise RuntimeError(f"GAP error: {error.strip()}")
    return output.strip()

def compute_holomorph(group_definition):
    gap_code = f"""
    G := {group_definition};
    A := AutomorphismGroup(G);
    H := SemidirectProduct(A, G);
    Display(H);
    Print("Order of Hol(G): ", Size(H), "\\n");
    """
    return run_gap_code(gap_code)

def sylow_p_subgroups_symmetric(n, p):
    gap_code = f"""
    G := SymmetricGroup({n});
    P := SylowSubgroup(G, {p});
    C := ConjugateSubgroups(G, P);
    Print("Total Sylow {p}-subgroups in S_{n}: ", Length(C), "\\n\\n");

    for i in [1..Length(C)] do
        Print("== Sylow {p}-subgroup #", i, " ==\\n");
        Display(C[i]);
        Print("Order: ", Size(C[i]), "\\n");

        # Compute Holomorph of this subgroup
        A := AutomorphismGroup(C[i]);
        H := SemidirectProduct(A, C[i]);
        Print("-- Holomorph of Sylow subgroup #", i, " --\\n");
        Display(H);
        Print("Order of Holomorph: ", Size(H), "\\n\\n");
    od;
    """

    print(gap_code)
    return run_gap_code(gap_code)

# === MAIN ===
if __name__ == "__main__":
    # # Holomorph of C4 (SmallGroup(4,1) ≅ Z4)
    # print("== Holomorph of SmallGroup(4,1) ==")
    # try:
    #     hol = compute_holomorph("SmallGroup(4,1)")
    #     print(hol)
    # except RuntimeError as e:
    #     print(f"Holomorph Error: {e}")

    # Sylow 3-subgroups of S_4
    print("\n== Sylow 3-subgroups of S_4 ==")
    try:
        syl = sylow_p_subgroups_symmetric(4, 3)
        print(syl)
    except RuntimeError as e:
        print(f"Sylow Error: {e}")

