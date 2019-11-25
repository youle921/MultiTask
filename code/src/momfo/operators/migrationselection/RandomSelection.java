package momfo.operators.migrationselection;

import momfo.core.SolutionSet;
import momfo.util.PseudoRandom;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

/**
 * This class implements an migration selection operator
 */
public class RandomSelection extends MigrationSelection {

    private int MigrationSize;
    private SolutionSet DestinationSolution;

    public RandomSelection(HashMap<String, Object> parameters) {
        super(parameters);
        MigrationSize = (int) parameters.get("MigrationSize");
    } // NeighborSelection

    /**
     * Performs the operation
     * 
     * @param object Object representing a SolutionSet
     * @return the selected solution
     */
    public Object execute(Object object) {
        SolutionSet MigrationSolution = (SolutionSet) object;
        
        List<Integer> index = new ArrayList<Integer>();
		for (int i = 0; i < MigrationSolution.getMaxSize(); i++) {
			index.add(i);
		}

		SolutionSet chosen_solution = new SolutionSet();
		for (int n = 0; n < MigrationSize; n++) {
			int rand_index = PseudoRandom.randInt(0, index.size() - 1);
			chosen_solution.add(MigrationSolution.get(index.remove(rand_index)));
		}

		return chosen_solution;
    } // execute

    public void setDestinationSolution(SolutionSet solution) {
        DestinationSolution = solution;
    }

} // RandonSelection
