package momfo.problems.knapsack;

import momfo.util.JMException;
import momfo.util.wrapper.XInt;
import momfo.core.Solution;

public class Knapsack_profitflip extends Knapsack {

    private int numberOfFlippingBits;

    public Knapsack_profitflip(Integer numberOfObjectives, double fr) {

        super(numberOfObjectives);
        problemName_ = "Knapsack_Profitflip";
        numberOfFlippingBits = (int) (numberOfVariables_ * fr);

        for (int i = 0; i < numberOfFlippingBits; i++){
            profit_[1][i] = 110 - profit_[1][i];
        }
    }
}

