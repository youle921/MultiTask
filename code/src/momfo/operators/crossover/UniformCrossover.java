//  SBXCrossover.java
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

package momfo.operators.crossover;

import momfo.core.Solution;
import momfo.core.SolutionType;
import momfo.core.Variable;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.encodings.solutionType.RealSolutionType;
import momfo.encodings.variable.Binary;
import momfo.util.Configuration;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.wrapper.XInt;
import momfo.util.wrapper.XReal;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * This class allows to apply a uniform crossover operator using two parent
 * solutions.
 */
public class UniformCrossover extends Crossover {

	/**
	 * EPS defines the minimum difference allowed between real values
	 */

	private Double crossoverProbability_ = 0.9;

	/**
	 * Valid solution types to apply this operator
	 */
	private static final List VALID_TYPES = Arrays.asList(RealSolutionType.class, IntSolutionType.class);

	/**
	 * Constructor Create a new uniform crossover operator whit a default index given by
	 * <code>DEFAULT_INDEX_CROSSOVER</code>
	 */
	public UniformCrossover(HashMap<String, Object> parameters) {
		super(parameters);

		if (parameters.get("probability") != null)
			crossoverProbability_ = (Double) parameters.get("probability");
	} // UniformCrossover

	/**
	 * Perform the crossover operation.
	 * 
	 * @param probability
	 *            Crossover probability
	 * @param parent1
	 *            The first parent
	 * @param parent2
	 *            The second parent
	 * @return An array containing the two offsprings
	 */
	public Solution[] doCrossover(double probability, Solution parent1, Solution parent2) throws JMException {

		int numberOfVariables = parent1.getNumberOfVariables();

		Solution[] offSpring = new Solution[2];
		offSpring[0] = new Solution(parent1);
		offSpring[1] = new Solution(parent2);

		XInt x1 = new XInt(parent1);
		XInt x2 = new XInt(parent2);

		XInt offSpring1 = new XInt(offSpring[0]);
		XInt offSpring2 = new XInt(offSpring[1]);

		if (PseudoRandom.randDouble() <= probability) {

			for (int i = 0; i < numberOfVariables; i++) {

				if (PseudoRandom.randDouble() <= 0.5) {
					offSpring1.setValue(i, x1.getValue(i));
					offSpring2.setValue(i, x2.getValue(i));
				} else {
					offSpring1.setValue(i, x2.getValue(i));
					offSpring2.setValue(i, x1.getValue(i));
				} // if
			} // if
		} // if

		return offSpring;
	} // doCrossover

	/**
	 * Executes the operation
	 * 
	 * @param object
	 *            An object containing an array of two parents
	 * @return An object containing the offSprings
	 */
	public Object execute(Object object) throws JMException {
		Solution[] parents = (Solution[]) object;

		if (parents.length != 2) {
			Configuration.logger_.severe("UniformCrossover.execute: operator needs two " + "parents");
			Class cls = java.lang.String.class;
			String name = cls.getName();
			throw new JMException("Exception in " + name + ".execute()");
		} // if

		if (!(VALID_TYPES.contains(parents[0].getType().getClass())
				&& VALID_TYPES.contains(parents[1].getType().getClass()))) {
			Configuration.logger_.severe("UniformCrossover.execute: the solutions " + "type " + parents[0].getType()
					+ " is not allowed with this operator");

			Class cls = java.lang.String.class;
			String name = cls.getName();
			throw new JMException("Exception in " + name + ".execute()");
		} // if

		Solution[] offSpring;
		offSpring = doCrossover(crossoverProbability_, parents[0], parents[1]);

		return offSpring;
	} // execute
} // SBXCrossover
