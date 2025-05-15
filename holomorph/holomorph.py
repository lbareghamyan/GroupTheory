from sympy import Matrix, Rational, gcd
import json

def parse_vector(vector_list, group_type, modulus=None):
    if group_type == "Q":
        return [Rational(x) for x in vector_list]
    else:
        return [int(x) % modulus if modulus else int(x) for x in vector_list]

def parse_matrix(matrix_list, group_type, modulus=None):
    mat = []
    for row in matrix_list:
        if group_type == "Q":
            mat.append([Rational(x) for x in row])
        else:
            mat.append([int(x) % modulus if modulus else int(x) for x in row])
    return Matrix(mat)

def build_holomorph_matrix(a, alpha):
    n = len(a)
    top_row = Matrix([[1] + a])
    return top_row.col_join(Matrix.hstack(Matrix.zeros(n, 1), alpha))

def is_in_gl_n(matrix, group_type, modulus=None):
    d = matrix.det()
    if group_type == "Z":
        return d == 1 or d == -1
    elif group_type == "Z_N":
        return gcd(int(d), modulus) == 1
    elif group_type == "Q":
        return d != 0
    return False

def pretty_print_matrix(mat):
    for row in mat.tolist():
        print("[ " + "  ".join(str(x) for x in row) + " ]")

def load_input_from_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def holomorph_product_from_file(file_path):
    data = load_input_from_file(file_path)
    n = data["num_factors"]
    group_type = data["group_type"].upper()
    modulus = data.get("modulus", None)

    elements = data["elements"]
    matrices = []

    for idx, el in enumerate(elements):
        a = parse_vector(el["a"], group_type, modulus)
        alpha = parse_matrix(el["alpha"], group_type, modulus)

        if not is_in_gl_n(alpha, group_type, modulus):
            print(f"❌ Matrix #{idx+1} is not a valid automorphism (not in GL_n).")
            return
        if group_type == "Z" and n == 1 and alpha[0] not in [1, -1]:
            print(f"❌ Invalid automorphism for Z at element #{idx+1}: must be ±1.")
            return

        matrices.append(build_holomorph_matrix(a, alpha))

    # Multiply all matrices in order
    product = matrices[0]
    for m in matrices[1:]:
        product *= m

    if group_type == "Z_N":
        product = product.applyfunc(lambda x: x % modulus)

    print("\n✅ Product of all holomorph elements =")
    pretty_print_matrix(product)

if __name__ == "__main__":
    holomorph_product_from_file("examples/holomorph_input_n10.json")
