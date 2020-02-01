package momfo.problems.knapsack;

public class Knapsack_scaling extends Knapsack {

    private double scaling_factor;
    public Knapsack_scaling(Integer numberOfObjectives, double sf) {

        super(numberOfObjectives);
        problemName_ = "Knapsack_Scaling";
        scaling_factor = sf;
        for (int i = 0; i < 2; i++){
            capacity_[i] *= scaling_factor;
        }
    }
}
