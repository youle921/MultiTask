//  UniformMutation.java
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

package momfo.operators.mutation;

import momfo.core.Solution;
import momfo.core.Variable;
import momfo.encodings.solutionType.IntSolutionType;
import momfo.encodings.solutionType.RealSolutionType;
import momfo.util.Configuration;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.wrapper.XInt;
import momfo.util.wrapper.XReal;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/**
 * This class implements a uniform mutation operator.
 */
public class BitFlipMutation extends Mutation {
	/**
	 * Valid solution types to apply this operator
	 */
	private static final List VALID_TYPES = Arrays.asList(RealSolutionType.class, IntSolutionType.class);
	/**
	 * Stores the value used in a uniform mutation operator
	 */

	private Double mutationProbability_ = null;

	/**
	 * Constructor Creates a new uniform mutation operator instance
	 */
	public BitFlipMutation(HashMap<String, Object> parameters) {
		super(parameters);

		if (parameters.get("probability") != null)
			mutationProbability_ = (Double) parameters.get("probability");

	} // UniformMutation

	/**
	 * Constructor Creates a new uniform mutation operator instance
	 */
	// public UniformMutation(Properties properties) {
	// this();
	// } // UniformMutation

	/**
	 * Performs the operation
	 * 
	 * @param probability
	 *            Mutation probability
	 * @param solution
	 *            The solution to mutate
	 * @throws JMException
	 */
	public void doMutation(double probability, Solution solution) throws JMException {
		
		XInt x = new XInt(solution);
		XInt var = new XInt(solution);

		for (int i = 0; i < solution.getNumberOfVariables(); i++) {
			if (PseudoRandom.randDouble() < probability) {
				x.setValue(i, 1 - var.getValue(i));
			} // if
			else{
				x.setValue(i, var.getValue(i));
			}
		} // for
	} // doMutation

	/**
	 * Executes the operation
	 * 
	 * @param object
	 *            An object containing the solution to mutate
	 * @throws JMException
	 */
	public Object execute(Object object) throws JMException {
		Solution solution = (Solution) object;

		if (!VALID_TYPES.contains(solution.getType().getClass())) {
			Configuration.logger_.severe("BitFlipMutation.execute: the solution "
					+ "is not of the right type. The type should be 'Real', but " + solution.getType()
					+ " is obtained");

			Class cls = java.lang.String.class;
			String name = cls.getName();
			throw new JMException("Exception in " + name + ".execute()");
		} // if

		doMutation(mutationProbability_, solution);

		return solution;
	} // execute
} // UniformMutation
