
%{
Datasets and Code for "Collaborative Filtering for Color Aesthetics" CAe 2014.
Peter O'Donovan and Aseem Agarwala and Aaron Hertzmann
 
Contact: Peter O'Donovan at <odonovan@dgp.toronto.edu>


Original PMF code  by Ruslan Salakhutdinov 
Permission is granted for anyone to copy, use, modify, or distribute this program and 
accompanying programs and documents for any purpose, provided this copyright notice is
 retained and prominently displayed, along with a note saying that the original programs 
are available from our web page. The programs and documents are distributed without any 
warranty, express or implied. As the programs were written for research purposes only, they 
have not been tested to the degree that would be advisable in any important application. All 
use of these programs is entirely at the user's own risk.

%}

clear all
load allMTurkRatings
load themeData


features=datapoints.features(:,1:334);


maxepoch=1000

paramList=[15 ];
paramTrainErr=zeros(length(paramList),maxepoch);
paramValidErr=zeros(length(paramList),maxepoch);


for l=1:length(paramList)

    epsilon_t=0.5;
    epsilon_p=0.5;
    lambda_t  = 0.01; % Regularization parameter 
    lambda_p  = 0.01; % Regularization parameter 
    momentum=0.8; 

    epoch=1; 


    mean_rating = mean(train_vec(:,3)); 

    pairs_tr = length(train_vec); % training data 
    pairs_pr = length(probe_vec); % validation data 

    numbatches= 3; % Number of batches  
    num_t = length(unique(train_vec(:,2)));  % Number of themes 
    num_p = length(unique(train_vec(:,1)));  % Number of users 
    num_feat = paramList(l); % Rank 10 decomposition 


    num_theme_feat=size(features,2);


    w1_P1     = 0.1*randn(num_p, num_feat); % User feature vecators
    w1_P1_inc = zeros(num_p, num_feat);




    %network layout
    nX = num_theme_feat;      % number of inputs
    nH = 200                 % number of hidden units
    nY = num_feat;            % number of outputs
    %nY = 1;            % number of outputs

    weight1 = rand(nX+1,nH)-0.5;
    weight2 = 0.1*rand(nH+1,nY)-0.05;
    weight3 = rand(nH+1,nY)-0.5;

    W=[weight1(:);weight2(:)];
    W_inc=zeros(size(W));

    nW1=length(weight1(:));
    nW2=length([weight1(:);weight2(:)]);

    weightInfo.w1=zeros(size(W));
    weightInfo.w1(1:nW1)=1;
    weightInfo.w1=weightInfo.w1==1;

    weightInfo.w2=zeros(size(W));
    weightInfo.w2(nW1+1:nW2)=1;
    weightInfo.w2=weightInfo.w2==1;

    weightInfo.w3=zeros(size(W));
    weightInfo.w3(nW2+1:length(W))=1;
    weightInfo.w3=weightInfo.w3==1;

    weightInfo.w1Size=size(weight1);
    weightInfo.w2Size=size(weight2);
    weightInfo.w3Size=size(weight3);

    
    err_train=zeros(1,maxepoch);
    err_valid=zeros(1,maxepoch);
    mae_train=zeros(1,maxepoch);
    mae_valid=zeros(1,maxepoch);


    for epoch = 1:maxepoch
      rr = randperm(pairs_tr);
      train_vec = train_vec(rr,:);

      clear rr 

      fprintf(1,'epoch %d batch ',epoch);
      for batch = 1:numbatches
        fprintf(1,'%d, ',batch);
        N=100000; % number training triplets per batch 

        aa_p   = double(train_vec((batch-1)*N+1:batch*N,1));
        aa_t   = double(train_vec((batch-1)*N+1:batch*N,2));
        rating = double(train_vec((batch-1)*N+1:batch*N,3));

        rating = rating-mean_rating; % Default prediction is the mean rating. 


        %for k=1:5

        dW=zeros(size(W));
         for ii=1:N/10000   
            range=((ii-1)*10000+1):(ii)*10000;
            feat=features(aa_t(range),:);
            user=w1_P1(aa_p(range),:);
            [Err, Grad] = bkpropColor( feat',user,rating(range)', W,weightInfo );

            dW=dW+Grad;
            errs(ii)=Err;

         end


        [er, gr, latentFeat] = bkpropColor( features',ones(num_feat,1), [], W,weightInfo  );


        %%%%%%%%%%%%%% Compute Predictions %%%%%%%%%%%%%%%%%
        pred_out = sum(latentFeat(aa_t,:) .*w1_P1(aa_p,:),2);

        f = sum((pred_out - rating).^2) + 0.5*lambda_p*( sum(sum( (w1_P1(aa_p,:).^2),2)));


        %%%%%%%%%%%%%% Compute Gradients %%%%%%%%%%%%%%%%%%%
        IO = repmat(2*(pred_out - rating),1,num_feat);

        Ix_p=IO.*latentFeat(aa_t,:) + lambda_p*w1_P1(aa_p,:);

        dw1_P1 = zeros(num_p,num_feat);

        for ii=1:N 
          dw1_P1(aa_p(ii),:) =  dw1_P1(aa_p(ii),:) +  Ix_p(ii,:);
        end


        %%%% Update weights and user features %%%%%%%%%%%

        W_inc = momentum*W_inc + epsilon_t*dW/N;
        W =  W - W_inc;

        w1_P1_inc = momentum*w1_P1_inc + epsilon_p*dw1_P1/N;
        w1_P1 =  w1_P1 - w1_P1_inc;

      end 

      %%%%%%%%%%%%%% Compute Predictions after Parameter Updates %%%%%%%%%%%%%%%%%
      [er, gr, latentFeat] = bkpropColor( features',ones(num_feat,1), [], W,weightInfo );
      pred_out = sum(latentFeat(aa_t,:) .*w1_P1(aa_p,:),2);
      f_s = sum( (pred_out - rating).^2);
      err_train(epoch) = sqrt(f_s/N);
      
      mae_train(epoch)=mean(abs(pred_out - rating));


      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      %%% Compute predictions on the validation set %%%%%%%%%%%%%%%%%%%%%% 
      NN=length(probe_vec);

      aa_p = double(probe_vec(:,1));
      aa_t = double(probe_vec(:,2));
      rating = double(probe_vec(:,3));
      

      NN=length(test_vec);
      aa_p = double(test_vec(:,1));
      aa_t = double(test_vec(:,2));
      rating = double(test_vec(:,3));
      

      pred_out = sum(latentFeat(aa_t,:) .*w1_P1(aa_p,:),2) + mean_rating;
      ff = find(pred_out>5); pred_out(ff)=5; % Clip predictions 
      ff = find(pred_out<1); pred_out(ff)=1;

      
      
      err_valid(epoch) = sqrt(sum((pred_out- rating).^2)/NN);
      mae_valid(epoch)=mean(abs(pred_out - rating));
      fprintf(1, 'Training RMSE %6.4f  Test RMSE %6.4f, Training MAE %6.4f  Test MAE %6.4f  \n',err_train(epoch), err_valid(epoch),mae_train(epoch), mae_valid(epoch));
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

      if (rem(epoch,10))==0
        paramTrainErr(l,:)=err_train;
        paramValidErr(l,:)=err_valid;
      end

    end 

end


        

        
      

    