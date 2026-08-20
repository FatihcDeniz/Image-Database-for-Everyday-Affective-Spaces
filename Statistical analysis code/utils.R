library(ggplot2)
library(irr)

qq_plot <- function(residuals, title) {
  # This function generates a quantile-quantile (Q-Q) plot for a vector of residuals using `ggplot2`. 
  
  ggplot(data.frame(res = residuals), aes(sample = res)) +
    stat_qq(size = 0.2, sample = 1000) +
    stat_qq_line() +
    labs(
      title = title,
      x = "Theoretical Quantiles",
      y = "Sample Quantiles"
    ) +
    theme_apa() +
    theme(
      plot.title = element_text(face = "bold", hjust = 0.5)
    )
}

check_create_directory <- function(path) {
  # Check whether a directory exist, otherwise create one,
  if (!dir.exists(path)) {
    dir.create(path, recursive = TRUE)
    message(sprintf("Directory created: %s", path))
  } else {
    message(sprintf("Directory already exists: %s", path))
  }
}

calculate_icc_scores_psych <- function(type = "ICC2k") {
  ## Calcualte ÏCC scores for all dependent variables and returns a table. You can see different types of ICC here https://www.rdocumentation.org/packages/psych/versions/2.6.1/topics/ICC
  icc_results <- data.frame(matrix(ncol = 4, nrow = 0))
  colnames(icc_results) <- c("Response", "ICC Value", "Lower Bound", "Upper Bound")
  # Valence  ----
  data_valence <- read.csv("..\\Data for ICC analysis\\icc_valence.csv")
  icc_results_valence <- psych::ICC(data_valence, missing = TRUE)
  icc_results[1,] = c("Valence", round(icc_results_valence$results[icc_results_valence$results$type == type,"ICC"],3), 
                      round(icc_results_valence$results[icc_results_valence$results$type == "ICC3k","lower bound"],3),
                      round(icc_results_valence$results[icc_results_valence$results$type == "ICC3k","upper bound"],3))
  
  # Approach  ----
  data_approach <- read.csv("..\\Data for ICC analysis\\icc_approach.csv")
  icc_results_approach <- psych::ICC(data_approach, missing = TRUE)
  icc_results[2,] = c("Approach-avoidance", round(icc_results_approach$results[icc_results_approach$results$type == type,"ICC"],3), 
                      round(icc_results_approach$results[icc_results_approach$results$type == "ICC3k","lower bound"],3),
                      round(icc_results_approach$results[icc_results_approach$results$type == "ICC3k","upper bound"],3))
  
  # Tense Arousal  ----
  data_t_arousal <- read.csv("..\\Data for ICC analysis\\icc_tense.csv")
  icc_results_t_arousal <- psych::ICC(data_t_arousal, missing = TRUE)
  icc_results[3,] = c("Tense Arousal", round(icc_results_t_arousal$results[icc_results_t_arousal$results$type == type,"ICC"],3), 
                      round(icc_results_t_arousal$results[icc_results_t_arousal$results$type == "ICC3k","lower bound"],3),
                      round(icc_results_t_arousal$results[icc_results_t_arousal$results$type == "ICC3k","upper bound"],3))
  
  # Energetic Arousal  ----
  data_e_arousal <- read.csv("..\\Data for ICC analysis\\icc_energetic.csv")
  icc_results_e_arousal <- psych::ICC(data_e_arousal, missing = TRUE)
  icc_results[4,] = c("Energetic Arousal", round(icc_results_e_arousal$results[icc_results_e_arousal$results$type == type,"ICC"],3), 
                      round(icc_results_e_arousal$results[icc_results_e_arousal$results$type == "ICC3k","lower bound"],3),
                      round(icc_results_e_arousal$results[icc_results_e_arousal$results$type == "ICC3k","upper bound"],3))
  
  return(icc_results)
}

regression_table <- function(model) {
  ## Helper function to automatically generate APA style regression tables. Takes a `lm` model as input.
  stats.table <- as.data.frame(summary(model)$coefficients)
  CI <- confint(lm.beta(model))
  stats.table <- cbind(row.names(stats.table), stats.table, CI)
  names(stats.table) <- c("Response", "Standardized Coefficients", "SE", "T", "p", "CI_lower", "CI_upper")
  stats.table <- stats.table[2:length(stats.table[, "Response"]),]
  standard_coef <- lm.beta(model)
  stats.table[, "Standardized Coefficients"] <- as.vector(standard_coef$standardized.coefficients[2:length(standard_coef$standardized.coefficients)])
  stats.table <- stats.table[,!colnames(stats.table) %in% c("T")]
  
  my_table <- rempsyc::nice_table(stats.table)
  return(my_table)
}

get_posterior_probs <- function(model1,model2,model3,model4,model5,model6,model7) {
  # Helper function to calculate Posterior probability for all seven models used in study.
  
  # Get BIC values for all models
  bic_vals <- c(
    model1 = BIC(model1),
    model2 = BIC(model2),
    model3 = BIC(model3),
    model4 = BIC(model4),
    model5 = BIC(model5),
    model6 = BIC(model6),
    model7 = BIC(model7)
  )
  
  # Calculate Posterior Probability.
  log_weights <- -0.5 * (bic_vals - min(bic_vals))
  weights <- exp(log_weights)
  posterior_probs <- weights / sum(weights)
  
  return(posterior_probs)
}

pred_scores <- function(models, data, col_names,length_out) {
  # Helper function to predict scores given a model.
  sequence_df <- seq(min(data), max(data), length.out = length_out) 
  sequence_df <- data.frame(score = sequence_df,
                            I = ifelse(sequence_df >= 0, 1, 0))
  
  colnames(sequence_df) <- col_names
  
  for (i in seq_along(models)) {
    sequence_df[[paste0("model_", i)]] <- predict(models[[i]], newdata = sequence_df)
  }
  
  return(sequence_df)
}

plot_data <- function(data, colnames, title_names, alpha_point, alpha_hvline, tick_size, title_size) {
  # Simple function for plotting

  plot <- ggplot(data, aes(x = .data[[colnames[1]]], 
                           y = .data[[colnames[2]]])) + 
    geom_point(alpha = alpha_point) +
    theme_apa() + 
    theme(
      axis.text.x  = element_text(size = tick_size),
      axis.text.y  = element_text(size = tick_size),
      axis.title.x = element_text(size = title_size, face = "bold"),
      axis.title.y = element_text(size = title_size, face = "bold")
    ) +
    xlab(title_names[1]) + 
    ylab(title_names[2]) + 
    geom_hline(yintercept = 0, alpha = alpha_hvline) + 
    geom_vline(xintercept = 0, alpha = alpha_hvline) + 
    scale_x_continuous(limits = c(-3, 3), breaks = seq(-3, 3, by = 1)) +
    scale_y_continuous(limits = c(-3, 3), breaks = seq(-3, 3, by = 1)) 
  
  return(plot)
}

add_lines <- function(data, model_names, plot, x_col = "valence", color_palette,size, alpha_val) {
  # Helper function to add lines for Figure 3 and Supplementary Section S5.
  for (i in 1:7) {
    nm <- paste0("model_", i)
    if (nm %in% model_names) {
      plot <- plot +
        geom_line(data = data,
                  aes_string(x = x_col, y = nm), color = color_palette[i], size = size, alpha = alpha_val)
    }
  }
  plot
}

get_sig_stars <- function(p) {
  # Helper function to add significance stars in tables.
  if (p < 0.001) return("***")
  else if (p < 0.01) return("**")
  else if (p < 0.05) return("*")
  else return("")
}

make_effects_table <- function(anova_res, dv_name) {
  # Helper function to create ANOVA tables given an anova model and dependent variable name. 
  data.frame(
    `Dependent Variable` = c(dv_name, rep("", nrow(anova_res) - 1)),
    `Full Model` = rownames(anova_res),
    `Numerator DF`  = round(anova_res$NumDF),
    `Denominator DF`  = round(anova_res$DenDF),
    F = sprintf("%.2f%s", anova_res$`F value`, sapply(anova_res$`Pr(>F)`, get_sig_stars)),
    `p` = round(anova_res$`Pr(>F)`,2),
    `Partial EtaSquared` = round(effectsize::eta_squared(anova_res)[["Eta2_partial"]],2),
    row.names = NULL
  )
}

extract_r2 <- function(model) {
  # Helper function to extract R2 marginal and conditional given a lme4 model.
  r2 <- performance::performance(model)
  data.frame(
    R2_marginal = round(r2$R2_marginal, 2),
    R2_conditional = round(r2$R2_conditional, 2)
  )
}

extract_skewness_kurtosis <- function(model) {
  # Helper functions to calculate skewness and kurtosis.
  res <- residuals(model)
  
  data.frame(
    Skewness = round(moments::skewness(res, na.rm = TRUE), 3),
    Kurtosis = round(moments::kurtosis(res, na.rm = TRUE), 3)
  )
}

extract_emm <- function(df, outcome_name) {
  # Helper function to extract estimated marginal means given the emmeans model and variable name
  df %>%
    select(room_type, emmean, SE) %>%
    mutate(
      Outcome = outcome_name,
      Mean = round(emmean, 2),
      SE = round(SE, 2)
    ) %>%
    select(Outcome, room_type, Mean, SE)
}

extract_welch_anova <- function(anova_res, dv_name) {
  # Helper function to extract Welch's ANOVa results
  data.frame(
    `Dependent Variable` = dv_name,
    `Numerator DF`  = anova_res$parameter[["num df"]],
    `Denominator DF`  = round(anova_res$parameter[["denom df"]], 2),
    `F`= round(anova_res$statistic[["F"]],2),
    `p` = anova_res$p.value,
    `Partial EtaSquared` = round(effectsize::eta_squared(anova_res)[["Eta2"]],2)
  )
}
