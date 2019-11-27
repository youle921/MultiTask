package momfo.operators.migrationselection;

import momfo.core.SolutionSet;
import momfo.util.Distance;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

/**
 * This class implements an binary tournament selection operator
 */
public class ShortestSelection extends MigrationSelection {

    private int MigrationSize;
    private SolutionSet DestinationSolution;

    private Distance distance = new Distance();

    public ShortestSelection(HashMap<String, Object> parameters) {
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
        SolutionSet chosenSolution = new SolutionSet(MigrationSize);

        List<Double> minList = new ArrayList<>(MigrationSolution.size());
        try {
            for (int i = 0; i < MigrationSolution.size(); i++) {
                minList.add(distance.distanceToSolutionSetInSolutionSpace(MigrationSolution.get(i), DestinationSolution));
            }
        } catch (momfo.util.JMException e) {
            return 0;
        }      

        int minIndex;
        for (int n = 0; n < MigrationSize; n++) {
            minIndex = minList.indexOf(Collections.min(minList));
            minList.set(minIndex, Double.MAX_VALUE);
            chosenSolution.add(MigrationSolution.get(minIndex));
        }

		return chosenSolution;
    } // execute

    public void setDestinationSolution(SolutionSet solution) {
        DestinationSolution = solution;
    }
} // NeighborSelection
