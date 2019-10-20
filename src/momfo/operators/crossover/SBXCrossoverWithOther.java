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

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import momfo.core.Solution;
import momfo.encodings.solutionType.RealSolutionType;
import momfo.util.Configuration;
import momfo.util.JMException;
import momfo.util.PseudoRandom;
import momfo.util.wrapper.XReal;

/**
 * This class allows to apply a SBX crossover operator using two parent
 * solutions.
 */
public class SBXCrossoverWithOther extends Crossover {
	
	/**
	 * EPS defines the minimum difference allowed between real values
	 */
	private static final double EPS = 1.0e-14;

	private static final double ETA_C_DEFAULT_ = 20.0;
	private Double crossoverProbability_ = 0.9;
	private double distributionIndex_ = ETA_C_DEFAULT_;

	private double SBXAlpha = 0.5;
	
	/**
	 * Valid solution types to apply this operator
	 */
	private static final List VALID_TYPES = Arrays.asList(RealSolutionType.class);

	/**
	 * Constructor Create a new SBX crossover operator whit a default index
	 * given by <code>DEFAULT_INDEX_CROSSOVER</code>
	 */
	// if SBX alphar = 0.5, each parents are selected as a parents.  
	public SBXCrossoverWithOther(HashMap<String, Object> parameters) {
		super(parameters);

		if (parameters.get("probability") != null)
			crossoverProbability_ = (Double) parameters.get("probability");
		if (parameters.get("distributionIndex") != null)
			distributionIndex_ = (Double) parameters.get("distributionIndex");
		
		if (parameters.get("SBXAlpha") != null)
			SBXAlpha = (Double) parameters.get("SBXAlpha");
		else 
			SBXAlpha = 0.5;
		
	} // SBXCrossover

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
		Solution[] offSpring = new Solution[2];

		offSpring[0] = new Solution(parent1);
		offSpring[1] = new Solution(parent2);

		int i;
		double rand;
		double y1, y2, yL, yu;
		double c1, c2;
		double alpha, beta, betaq;
		double valueX1, valueX2;
		XReal x1 = new XReal(parent1);
		XReal x2 = new XReal(parent2);
		XReal offs1 = new XReal(offSpring[0]);
		XReal offs2 = new XReal(offSpring[1]);

		int numberOfVariables = x1.getNumberOfDecisionVariables();

		if (PseudoRandom.randDouble() <= probability) {
				for (i = 0; i < numberOfVariables; i++) {
					double u = PseudoRandom.randDouble();
					double cf = 0;

					if (u <= 0.5) {
						cf = Math.pow(2.0 * u, 1.0 / (distributionIndex_ + 1.0));
					} else if (u > 0.5) {
						cf = Math.pow(2.0 * (1.0 - u), -1.0 / (distributionIndex_+ 1.0));
					} else {
						throw new JMException("something is wrong");
					}

					double val_1 = 0.5 * ((1 + cf) * parent1.getDecisionVariables()[i].getValue() + (1 - cf) * parent2.getDecisionVariables()[i].getValue());
					if (val_1 > 1.0)
						val_1 = 1.0;
					else if (val_1 < 0.0)
						val_1 = 0.0;
					double val_2 = 0.5 * ((1 + cf) * parent2.getDecisionVariables()[i].getValue() + (1 - cf) * parent1.getDecisionVariables()[i].getValue());
					if (val_2 > 1.0)
						val_2 = 1.0;
					else if (val_2 < 0.0)
						val_2 = 0.0;

					if (PseudoRandom.randDouble() < SBXAlpha) {
						offSpring[0].getDecisionVariables()[i].setValue(val_2);
						offSpring[1].getDecisionVariables()[i].setValue(val_1);
					} else {
						offSpring[0].getDecisionVariables()[i].setValue(val_1);
						offSpring[1].getDecisionVariables()[i].setValue(val_2);
					}
				}		
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
			Configuration.logger_.severe("SBXCrossover.execute: operator needs two " + "parents");
			Class cls = java.lang.String.class;
			String name = cls.getName();
			throw new JMException("Exception in " + name + ".execute()");
		} // if

		if (!(VALID_TYPES.contains(parents[0].getType().getClass())
				&& VALID_TYPES.contains(parents[1].getType().getClass()))) {
			Configuration.logger_.severe("SBXCrossover.execute: the solutions " + "type " + parents[0].getType()
					+ " is not allowed with this operator");

			Class cls = java.lang.String.class;
			String name = cls.getName();
			throw new JMException("Exception in " + name + ".execute()");
		} // if

		Solution[] offSpring;
		offSpring = doCrossover(crossoverProbability_, parents[0], parents[1]);

		// for (int i = 0; i < offSpring.length; i++)
		// {
		// offSpring[i].setCrowdingDistance(0.0);
		// offSpring[i].setRank(0);
		// }
		return offSpring;
	} // execute
} // SBXCrossover
