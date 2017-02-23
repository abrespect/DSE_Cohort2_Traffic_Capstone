package org.ucsd.dse.capstone.traffic

import java.io.BufferedReader
import java.io.FileReader
import scala.collection.mutable.ListBuffer
import org.apache.spark.SparkContext
import org.apache.spark.annotation.Since
import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.regression.RandomForestRegressionModel
import org.apache.spark.ml.regression.RandomForestRegressor
import org.apache.spark.mllib.linalg.SparseVector
import org.apache.spark.sql.SQLContext
import java.io.IOException

/**
 * Executes RandomForestRegressor against specified data
 *
 * @author dyerke
 */
class RandomForestRegressorExecutor(path: String, label_column_name: String = "AGG_TOTAL_FLOW", whiten: Boolean = true) extends Executor[RegressorResult] {

  override def execute(sc: SparkContext, sql_context: SQLContext, args: String*): RegressorResult = {
    var header_row: String = null
    var br: BufferedReader = null
    try {
      br = new BufferedReader(new FileReader(path))
      header_row = br.readLine()
    } catch {
      case e: IOException => throw new IllegalStateException(e)
    } finally {
      if (br != null) {
        br.close()
      }
    }
    //
    // create DataFrame
    //
    val (df, feature_column_name, column_names) = IOUtils.parse_preprocessed(sc, sql_context, path, header_row, label_column_name, whiten)
    //
    // execute RandomForestRegressor
    //
    val Array(trainingData, testData) = df.randomSplit(Array(0.7, 0.3))
    val regressor: RandomForestRegressor = new RandomForestRegressor()
    regressor.setLabelCol(label_column_name).setFeaturesCol(feature_column_name)
    //
    // Train
    //
    val model: RandomForestRegressionModel = regressor.fit(trainingData)
    //
    // Predict
    //
    val predictions = model.transform(testData)

    // Select example rows to display.
    predictions.select("prediction", label_column_name, feature_column_name).show(5)

    // Select (prediction, true label) and compute test error
    val evaluator = new RegressionEvaluator()
      .setLabelCol(label_column_name)
      .setPredictionCol("prediction")
      .setMetricName("r2")
    //
    val score = evaluator.evaluate(predictions)
    println("R2 Score on test data = " + score)
    //
    // feature importance
    //
    val out_list: ListBuffer[Tuple2[String, Double]] = new ListBuffer[Tuple2[String, Double]]()
    val fi: SparseVector = model.featureImportances.asInstanceOf[SparseVector]
    fi.foreachActive { (a_idx, a_val) =>
      val feature_name: String = column_names(a_idx)
      val feature_rate: Double = a_val
      val new_entry: Tuple2[String, Double] = (feature_name, feature_rate)
      out_list += new_entry
    }
    val sorted_feature_importance_list = out_list.sortWith { (left, right) =>
      left._2 > right._2
    }.toList
    return new RegressorResult(score, sorted_feature_importance_list)
  }
}