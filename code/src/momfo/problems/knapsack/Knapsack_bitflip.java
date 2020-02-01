package momfo.problems.knapsack;

import momfo.util.JMException;
import momfo.util.wrapper.XInt;
import momfo.core.Solution;

public class Knapsack_bitflip extends Knapsack {

    private int numberOfFlippingBits;

    public Knapsack_bitflip(Integer numberOfObjectives, double fr) {

        super(numberOfObjectives);
        problemName_ = "Knapsack_Bitflip";
        numberOfFlippingBits = (int) (numberOfVariables_ * fr);
    }

    public void evaluate(Solution solution) throws JMException {

        XInt var = new XInt(solution);
        int[] f = new int[numberOfObjectives_];

        repair(var);

        int sum;
        for (int i = 0; i < numberOfObjectives_; i++) {
            sum = 0;

            for (int j = 0; j < numberOfFlippingBits; j++) {
                sum += profit_[i][j] * (1 - var.getValue(j));
            }
            for (int j = numberOfFlippingBits ; j < numberOfVariables_; j++){
                sum += profit_[i][j] * var.getValue(j);
            }

            f[i] = sum;
        }

        // to change to minimization problems, use objective function value multipled by
        // -1
        for (int i = 0; i < numberOfObjectives_; i++) {
            solution.setObjective(i, -1 * f[i]);
        }
    }

    public void repair(XInt v) throws JMException {

        int idx;

        for (int counter = 0; break_knapsack(v); counter++) {
            idx = sort_min_[counter];
            if (idx < numberOfFlippingBits) {
                v.setValue(idx, 1);
            } else {
                v.setValue(idx, 0);
            }
        }

    }

    /*
     * if at least one Knapsack is broken, this method return true; else return
     * false;
     */
    public boolean break_knapsack(XInt sol) throws JMException {

        double sum;

        for (int i = 0; i < numberOfObjectives_; i++) {

            sum = 0;

            for (int j = 0; j < numberOfFlippingBits; j++) {
                sum += weight_[i][j] * (1 - sol.getValue(j));
            }
            for (int j = numberOfFlippingBits ; j < numberOfVariables_; j++){
                sum += weight_[i][j] * sol.getValue(j);
            }

            if (sum > capacity_[i]) {
                return true;
            }
        }
        return false;
    }
}
