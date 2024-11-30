# The max is the largest set of vertices such that any two of them are adjacent. We are going to apply
# different values for k (size of the max clique), k={1,2,...,n} and then check using SAT solver do such clique exist.

class CliqueSATEncoder:
    graph_edges = []
    v = 0
    clauses = []
    num_vars = 0
    k = 0

    def pos_constraints(self):
        for i in range(1, self.k + 1):
            for v in range(1, self.v + 1):
                for w in range(v + 1, self.v + 1):  
                    self.clauses.append([-((v - 1)*self.k + i), -((w - 1)*self.k + i)])

    def v_constraints(self):
        for v in range(1, self.v + 1):
            for i in range(1, self.k + 1): 
                for j in range(i + 1, self.k + 1):
                    self.clauses.append([-((v - 1)*self.k + i), -((v - 1)*self.k + j)])

    def occ_constraints(self):
        for i in range(1, self.k + 1):
            self.clauses.append([(v - 1)*self.k + i for v in range(1, self.v + 1)])

    def e_constraints(self):
        for i in range(1, self.k):  
            for j in range(i + 1, self.k + 1):
                for v in range(1, self.v + 1): 
                    for w in range(1, self.v + 1):
                        if v != w and ((v, w) not in self.graph_edges) and ((w, v) not in self.graph_edges):
                            self.clauses.append([-((v - 1)*self.k + i), -((w - 1)*self.k + j)])

    def generate_cnf(self, edges, v, k):
        self.k = k
        self.graph_edges = edges
        self.v = v
        self.clauses = []
        self.num_vars = self.v * k

        self.pos_constraints()
        self.v_constraints()
        self.occ_constraints()
        self.e_constraints()

        dimacs = f"p cnf {self.num_vars} {len(self.clauses)}\n"
        for clause in self.clauses:
            dimacs += " ".join(map(str, clause)) + " 0\n"
            
        return dimacs 



def main():
    edges = [(1, 2), (2, 3), (3, 4), (4, 1), (3, 5), (4, 5)] 
    v = 5  
    k = 3 

    encoder = CliqueSATEncoder()
    cnf = encoder.generate_cnf(edges, v, k)

    print(cnf)

    with open("problem.cnf", "w") as f:
        f.write(cnf) 

if __name__ == "__main__":
    main()