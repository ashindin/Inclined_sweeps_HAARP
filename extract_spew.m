%% extract_spew.m  % 4/1/10 P.A. Roddy
clear all
close all
fclose('all');

%% select output length and directory
tic

%home_dir = 'J:\Bernhard\30032011\';
%home_dir = '..\data\';

% % name of output directory
% spew_segment_dir = ['spew_segments']; %

%% some setup stuff

% select the file to open
% [fname, pathname] = uigetfile('*.DRXS12', 'Select A Data File For Analysis',home_dir);
filelist= dir('*.DRXS12');
%[fname, pathname] = uigetfile( ...
%    {'*.DRXS12'}, ...
%    'Select A Data File For Analysis', home_dir,...
%    'MultiSelect', 'on');

%if iscell(fname)~=1
%    temp=fname;
%    fname=cell(1);
%    fname{1}=temp;
%    clear temp
%end
num_of_files=length(filelist);
%fname=sort(fname);

for N_file=1:num_of_files
    %%%%%%%%
    output_file_length = 1.0;
    fprintf('\n')
    %fprintf([fname{N_file} '\n'])
    fprintf([filelist(N_file).name '\n']);
    fname_load=filelist(N_file).name;
    %fname_load=strcat(pathname,fname{N_file});
    %%%%%%%%
    % open the file to get the start time
    tsof=gettsofspew(fname_load);
    tsof.s=tsof.s;
    handles.Ninit=[tsof.y tsof.m tsof.d tsof.h tsof.min tsof.s];
    
    % open the file and get the length of the file in seconds (and other stuff)
    [z,rxinfo,vdflag,rdinfo,onepps]=rddrxspew(fname_load,handles.Ninit,1,'n',1);
    
    %% chop up the file
    %duration of original file in sec
    file_duration = datenum(rdinfo.DataNTPEndTime - rdinfo.DataNTPStartTime)*86400;
    
    %number of chunks of output file
    num_chunks = ceil(file_duration/output_file_length);
    fprintf(['The parent spew file is ' num2str(file_duration) ' seconds long.\n'])
    fprintf(['This will create ' num2str(num_chunks) ', ' num2str(output_file_length) ' second long files.\n'])
    
    % loop to create chunks
    file_save=[fname_load '.raw'];
    [File, mes]=fopen(file_save, 'w');
    % fname_mat=cell(num_chunks,1);
    
    %Wait = waitbar(0,'Saving...');
    for i = 1:num_chunks
        
        time_vec = handles.Ninit; %file start time
        time_vec(6) = time_vec(6) + output_file_length*(i-1); %time to start reading file for a given chunk
        
        % determine if data is request beyond length of file. Ask for less if
        % it is.
        if  (datenum(rdinfo.DataNTPEndTime) -  datenum(time_vec))*86400 <= output_file_length
            
            output_file_length =  (datenum(rdinfo.DataNTPEndTime) -  datenum(time_vec))*86400 - .25;
            
        end
        
        [z,rxinfo,vdflag,rdinfo,onepps]=rddrxspew(fname_load,time_vec,output_file_length,'n',512); %read the data
        
        %     % cd into data directory; create one if it doesnt exist
        %     try
        %         cd([home_dir '\' spew_segment_dir])
        %     catch
        %         fprintf(['Creating data directory "' spew_segment_dir '".\n'])
        %         mkdir(spew_segment_dir)
        %         cd([home_dir '\' spew_segment_dir])
        %     end
        
        
        onepps = logical(onepps); %convert onepps from uint32 to logical to save space
        
        %     if i<10
        %     fname_mat{i}=[fname '.part_0' num2str(i) '.mat'];
        %     else
        %     fname_mat{i}=[fname '.part_' num2str(i) '.mat'];
        %     end
        
        Z_save=[real(z) imag(z)];
        fwrite(File, Z_save', 'int32');
        %waitbar(i/num_chunks,Wait,strcat(num2str(i),'/',num2str(num_chunks)));
        %     save(fname_mat{i},'z','rxinfo','vdflag','rdinfo','onepps') %save the chunk to a .mat file
        %         fprintf(['part ' num2str(i) '\n'])
        %     cd(home_dir)
        
    end
    %close(Wait);
    %     clear oneopps spew_seg* time_vec  vdflag  handles i
    clear oneopps  output*  spew_seg* time_vec handles i
    toc
end
fclose('all');

