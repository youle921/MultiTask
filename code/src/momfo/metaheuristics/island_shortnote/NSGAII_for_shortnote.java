//  NSGAII.java
//
//  Author:
//       Antonio J. Nebro <antonio@lcc.uma.es>
//       Juan J. Durillo <durillo@lcc.uma.es>
//
//  Copyright (c) 2011 Antonio J. Nebro, Juan J. Durillo
//
//  This program is free software: you can redistribute it and/or modify
//  it under the terms of the GNU Lesser General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  This program is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU Lesser General Public License for more details.
//
//  You should have received a copy of the GNU Lesser General Public License
//  along with this program.  If not, see <http://www.gnu.org/licenses/>.

package momfo.metaheuristics.island_shortnote;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;

import momfo.core.Algorithm;
import momfo.core.Operator;
import momfo.core.ProblemSet;
import momfo.core.Solution;
import momfo.core.SolutionSet;
import momfo.operators.migrationselection.MigrationSelection;
import momfo.util.Distance;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.Ranking;
import momfo.util.comparators.CrowdingComparator;
import momfo.util.offspring.Offspring;

/**
 * Implementation of NSGA-II. This implementation of NSGA-II makes use of a
 * QualityIndicator object to obtained the convergence speed of the algorithm.
 * This version is used in the paper: A.J. Nebro, J.J. Durillo, C.A. Coello
 * Coello, F. Luna, E. Alba "A Study of Convergence Speed in Multi-Objective
 * Metaheuristics." To be presented in: PPSN'08. Dortmund. September 2008.
 */

public class NSGAII_for_shortnote extends Algorithm {
	/**
	 * Constructor
	 *
	 * @param problem Problem to solve
	 */

	private String[] path = new String[2];

	private int populationSize;
	private int evaluations;
	private int maxEvaluations;

	private int interval;
	private int size;
	private boolean criterion;

	private SolutionSet population;

	private Operator mutationOperator;
	private Operator crossoverOperator;
	private Operator selectionOperator;
	private Operator migrationOperator;

	private Distance distance = new Distance();

	Function<Solution, Solution> migrationParentSelection;

	public NSGAII_for_shortnote(ProblemSet problemSet) {
		super(problemSet);
		// System.out.println("sup: " + problemSet_.get(0).getHType());
	} // NSGAII

	/**
	 * Runs the NSGA-II algorithm.
	 *
	 * @return a <code>SolutionSet</code> that is a set of non dominated solutions
	 *         as a result of the algorithm execution
	 * @throws JMException
	 */

	public void initialize_island() throws JMException, ClassNotFoundException {

		populationSize = ((Integer) getInputParameter("populationSize")).intValue();
		maxEvaluations = ((Integer) getInputParameter("maxEvaluations")).intValue();

		// Read the operators
		mutationOperator = operators_.get("mutation");
		crossoverOperator = operators_.get("crossover");
		selectionOperator = operators_.get("selection");
		migrationOperator = operators_.get("migration");

		// Read migration parameters
		interval = ((Integer) getInputParameter("MigrationInterval")).intValue();
		size = ((Integer) getInputParameter("MigrationSize")).intValue();
		if (((String) getInputParameter("MigrationParentSelection")).equalsIgnoreCase("Random")) {
			migrationParentSelection = this::RandomMating;
		} else if (((String) getInputParameter("MigrationParentSelection")).equalsIgnoreCase("Neighbor")) {
			migrationParentSelection = this::NeighborMating;
		}

		// Initialize the variables
		population = new SolutionSet(populationSize);
		evaluations = 0;
		criterion = false;

		// Create the initial solutionSet
		Solution newSolution;
		for (int i = 0; i < populationSize; i++) {
			newSolution = new Solution(problemSet_);
			problemSet_.get(0).evaluate(newSolution);
			problemSet_.get(0).evaluateConstraints(newSolution);
			evaluations++;
			population.add(newSolution);
		} // for

		((MigrationSelection) migrationOperator).setDestinationSolution(population);

		// population.printVariablesToFile(path[0] + "/init_pops/var/pops" + path[1] +
		// ".dat");
		// population.printObjectivesToFile(path[0] + "/init_pops/obj/pops" + path[1] +
		// ".dat");

	}

	// GA execution methods
	public SolutionSet execute() throws JMException, ClassNotFoundException {

		SolutionSet offspringPopulation;
		SolutionSet union;

		// Generations
		int g = 1;
		while (evaluations < maxEvaluations & g < interval) {

			offspringPopulation = get_offspring(population);
			// Create the solutionSet union of solutionSet and offSpring
			union = ((SolutionSet) population).union(offspringPopulation);

			population = environmental_selection(union, populationSize);
			g++;
		} // while

		// population.printVariablesToFile(path[0] + "/final_pops/var/pops" + path[1] +
		// ".dat");
		// population.printObjectivesToFile(path[0] + "/final_pops/obj/pops" + path[1] +
		// ".dat");

		return population;

	} // execute

	public void migration_gen(SolutionSet migrated_pop) throws JMException {

		SolutionSet parent_pool = environmental_selection(population, populationSize - size);
		SolutionSet offspring = get_offspring(parent_pool, populationSize - size);

		SolutionSet chosenPopulation = (SolutionSet) migrationOperator.execute(migrated_pop);

		for (int ms = 0; ms < chosenPopulation.size(); ms++) {

			if (evaluations >= maxEvaluations) {
				criterion = true;
				break;
			}

			Solution parent1 = (new Solution(problemSet_, chosenPopulation.get(ms).getDecisionVariables()));
			offspring.add(migration_crossover(parent1, parent_pool));

		}

		SolutionSet union = ((SolutionSet) population).union(offspring);
		population = environmental_selection(union, populationSize);

	}

	// GA oprators
	private SolutionSet get_offspring(SolutionSet parent_pop) throws JMException {

		return get_offspring(parent_pop, populationSize);
	}

	private SolutionSet get_offspring(SolutionSet parent_pop, int offspring_size) throws JMException {

		SolutionSet offspring_population = new SolutionSet();

		Solution[] parents = new Solution[2];

		for (int i = 0; i < (offspring_size / 2); i++) {
			if (evaluations < maxEvaluations) {
				// obtain parents
				parents[0] = (Solution) selectionOperator.execute(parent_pop);
				parents[1] = (Solution) selectionOperator.execute(parent_pop);
				Solution[] offSpring = (Solution[]) crossoverOperator.execute(parents);
				mutationOperator.execute(offSpring[0]);
				mutationOperator.execute(offSpring[1]);
				problemSet_.get(0).evaluate(offSpring[0]);
				problemSet_.get(0).evaluateConstraints(offSpring[0]);
				problemSet_.get(0).evaluate(offSpring[1]);
				problemSet_.get(0).evaluateConstraints(offSpring[1]);
				offspring_population.add(offSpring[0]);
				offspring_population.add(offSpring[1]);
				evaluations += 2;
			} else {
				criterion = true;
			} // if
		} // for

		return offspring_population;

	}

	private SolutionSet environmental_selection(SolutionSet union, int pop_size) {

		// Ranking the union
		Ranking ranking = new Ranking(union);

		int remain = pop_size;
		int index = 0;
		SolutionSet front = null;
		SolutionSet selected_solutions = new SolutionSet();

		// Obtain the next front
		front = ranking.getSubfront(index);

		while ((remain > 0) && (remain >= front.size())) {

			// Add the individuals of this front
			distance.crowdingDistanceAssignment(front, problemSet_.get(0).getNumberOfObjectives());
			for (int k = 0; k < front.size(); k++) {
				selected_solutions.add(front.get(k));
			} // for

			// Decrement remain
			remain = remain - front.size();

			// Obtain the next front
			index++;
			if (remain > 0) {
				front = ranking.getSubfront(index);
			} // if
		} // while

		// Remain is less than front(index).size, insert only the best one
		if (remain > 0) { // front contains individuals to insert
			distance.crowdingDistanceAssignment(front, problemSet_.get(0).getNumberOfObjectives());
			front.shuffle();
			front.sort(new CrowdingComparator());

			SolutionSet f = new SolutionSet(remain);
			for (int k = 0; k < remain; k++) {
				f.add(front.get(k));
			} // for

			distance.crowdingDistanceAssignment(f, problemSet_.get(0).getNumberOfObjectives());
			f.sort(new CrowdingComparator());
			for (int k = 0; k < remain; k++) {
				selected_solutions.add(f.get(k));
			} // for

		} // if

		return selected_solutions;

	}

	// migration crossover
	public Solution migration_crossover(Solution parent1, SolutionSet candidate) throws JMException {

		Solution[] parents = new Solution[2];
		Solution[] offSpring = new Solution[2];

		if (evaluations < maxEvaluations) {
			// obtain parents
			parents[1] = parent1;
			parents[0] = migrationParentSelection.apply(parent1);
			offSpring = (Solution[]) crossoverOperator.execute(parents);
			mutationOperator.execute(offSpring[0]);
			problemSet_.get(0).evaluate(offSpring[0]);
			problemSet_.get(0).evaluateConstraints(offSpring[0]);
			evaluations ++;
		} else {
			criterion = true;
		} // if

		return offSpring[0];
	}

	public Solution RandomMating(Solution query) {

		int index = PseudoRandom.randInt(0, populationSize - 1);
		return population.get(index);
	}

	public Solution NeighborMating(Solution query) {

		int index = distance.indexToNearestSolutionInSolutionSpace(query, population);
		return population.get(index);
	}

	// Other operation
	public SolutionSet get_migrate_pop() {

		List<Integer> index = new ArrayList<Integer>();
		for (int i = 0; i < populationSize; i++) {
			index.add(i);
		}

		SolutionSet chosen_solution = new SolutionSet();
		for (int n = 0; n < size; n++) {
			int rand_index = PseudoRandom.randInt(0, index.size() - 1);
			chosen_solution.add(population.get(index.remove(rand_index)));
		}

		return chosen_solution;

	}

	public void setPath(String p, int no) {
		path[0] = p;
		path[1] = String.valueOf(no);
	}

	public SolutionSet get_front() {
		Ranking ranking = new Ranking(population);
		return ranking.getSubfront(0);
	}

	public SolutionSet get_all_pop() {

		SolutionSet allPopulation = new SolutionSet(populationSize);

		for (int i = 0; i < populationSize; i++) {
			allPopulation.add(population.get(i));
		}

		return allPopulation;
	}

	public boolean get_criterion() {
		return criterion;
	}
} // NSGA-II
